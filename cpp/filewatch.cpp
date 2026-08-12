#define _WIN32_WINNT 0x0A00
#define _WIN32_IE 0x0A00
#include "pipe.hpp"
#include "usn.hpp"
#include <iostream>
#include <thread>
#include <vector>
#include <string>

HANDLE g_stopEvent = NULL;

std::vector<std::wstring> GetNtfsDrives() {
    std::vector<std::wstring> drives;
    DWORD drivesMask = GetLogicalDrives();
    
    for (int i = 0; i < 26; i++) {
        if (drivesMask & (1 << i)) {
            wchar_t drive[4] = { L'A' + i, L':', L'\\', L'\0' };
            wchar_t fileSystemName[MAX_PATH];
            
            if (GetVolumeInformationW(drive, NULL, 0, NULL, NULL, NULL,
                fileSystemName, MAX_PATH)) {
                if (_wcsicmp(fileSystemName, L"NTFS") == 0) {
                    drives.push_back(std::wstring(1, L'A' + i) + L":");
                }
            }
        }
    }
    return drives;
}

std::string WStringToString(const std::wstring& wstr) {
    if (wstr.empty()) return std::string();
    
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), 
        (int)wstr.length(), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), (int)wstr.length(),
        &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

int main(){
    g_stopEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
    auto drives = GetNtfsDrives();
    auto eventHandler = [](short reasonType, const std::wstring& drive, const std::wstring& fullPath) {
        printf("Catched file: %s\n", WStringToString(fullPath).c_str());
        std::function<void()> tryit;
        tryit = [&fullPath, &tryit](){
            try {
                PipeClient filewatchClient("PSL_SAFE_FILE_WATCH_SERVER");
                std::string message;
                message = "catch_" + WStringToString(fullPath);
                filewatchClient.connect([&message](
                    std::function<std::string()> read,
                    std::function<void(const std::string&)> write,
                    std::function<void()> disconnect
                ) {
                    write(message);
                    disconnect();
                });
            } catch (const std::exception& e) {
                Sleep(20);
                tryit();
            }
        };
        tryit();
    };

    std::vector<std::thread> threads;
    for (const auto& drive : drives) {
        std::wstring volumePath = L"\\\\.\\" + drive;

        HANDLE hVolume = CreateFileW(
            volumePath.c_str(),
            GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            NULL,
            OPEN_EXISTING,
            FILE_FLAG_BACKUP_SEMANTICS,
            NULL
        );

        if (hVolume != INVALID_HANDLE_VALUE) {
            USN_JOURNAL_DATA journalData = {0};
            DWORD bytesReturned = 0;
            if (DeviceIoControl(hVolume, FSCTL_QUERY_USN_JOURNAL, 
                NULL, 0, &journalData, sizeof(journalData), 
                &bytesReturned, NULL)) {
                threads.emplace_back([volumePath, eventHandler, startUsn = journalData.NextUsn]() {
                    MonitorDrive(volumePath.c_str(), startUsn, eventHandler);
                });
            }
            CloseHandle(hVolume);
        }
    }

    WaitForSingleObject(g_stopEvent, INFINITE);

    g_running = false;
    for (auto& t : threads) {
        if (t.joinable()) t.join();
    }

    CloseHandle(g_stopEvent);
    return 0;
}