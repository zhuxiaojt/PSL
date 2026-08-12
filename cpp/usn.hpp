#include <windows.h>
#include <winioctl.h>
#include <stdio.h>
#include <atomic>
#include <functional>
#include <string>

std::atomic<bool> g_running(true);

std::wstring GetFullPathFromFRN(HANDLE hVolume, DWORD64 frn) {
    FILE_ID_DESCRIPTOR fid = {0};
    fid.dwSize = sizeof(FILE_ID_DESCRIPTOR);
    fid.Type = FileIdType;
    fid.FileId.QuadPart = frn;

    HANDLE hFile = OpenFileById(
        hVolume,
        &fid,
        0,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        NULL,
        FILE_FLAG_BACKUP_SEMANTICS
    );

    if (hFile == INVALID_HANDLE_VALUE) {
        return L"";
    }

    WCHAR path[MAX_PATH];
    DWORD result = GetFinalPathNameByHandleW(
        hFile,
        path,
        MAX_PATH,
        VOLUME_NAME_DOS
    );

    CloseHandle(hFile);

    if (result > 0 && result < MAX_PATH) {
        return std::wstring(path);
    }
    return L"";
}

int MonitorDrive(const LPCWSTR drive, DWORD64 startUsn,
                 std::function<void(const short, const std::wstring, const std::wstring)> callback) {
    HANDLE hVolume = CreateFileW(
        drive,
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
    );

    if (hVolume == INVALID_HANDLE_VALUE) {
        printf("CreateFileW failed with error %d\n", GetLastError());
        return 1;
    }

    USN_JOURNAL_DATA journalData = {0};
    DWORD bytesReturned = 0;
    DWORD64 currentUsn = startUsn;
    BYTE buffer[65536];
    READ_USN_JOURNAL_DATA_V0 readData = {0};


    if (!DeviceIoControl(hVolume, FSCTL_QUERY_USN_JOURNAL, NULL, 0,
        &journalData, sizeof(journalData), &bytesReturned, NULL)) {
        printf("FSCTL_QUERY_USN_JOURNAL failed with error %d\n", GetLastError());
        CloseHandle(hVolume);
        return 1;
    }
    while (g_running) {
        readData.StartUsn = currentUsn;
        readData.ReasonMask = 0xFFFFFFFF;
        readData.ReturnOnlyOnClose = 0;
        readData.Timeout = 5000;
        readData.BytesToWaitFor = 0;
        readData.UsnJournalID = journalData.UsnJournalID;

        if (!DeviceIoControl(hVolume, FSCTL_READ_USN_JOURNAL,
            &readData, sizeof(readData), buffer, sizeof(buffer),
            &bytesReturned, NULL)) {
            DWORD err = GetLastError();
            if (err == ERROR_JOURNAL_ENTRY_DELETED) {
                DeviceIoControl(hVolume, FSCTL_QUERY_USN_JOURNAL, NULL, 0,
                    &journalData, sizeof(journalData), &bytesReturned, NULL);
                currentUsn = journalData.FirstUsn;
                continue;
            }
            Sleep(100);
            continue;
        }

        if (bytesReturned < sizeof(DWORD64)) {
            Sleep(100);
            continue;
        }

        DWORD64 lastUsn = *(DWORD64*)buffer;
        USN_RECORD_V2* pRecord = (USN_RECORD_V2*)((BYTE*)buffer + sizeof(DWORD64));
        DWORD recordAreaSize = bytesReturned - sizeof(DWORD64);

        while (recordAreaSize > 0 && pRecord->RecordLength > 0) {
            if (pRecord->MajorVersion < 2 || pRecord->MajorVersion > 3) {
                recordAreaSize -= pRecord->RecordLength;
                pRecord = (USN_RECORD_V2*)((BYTE*)pRecord + pRecord->RecordLength);
                continue;
            }

            if (pRecord->FileNameLength > 0) {
                PWSTR fileName = (PWSTR)((BYTE*)pRecord + pRecord->FileNameOffset);
                DWORD fileNameLen = pRecord->FileNameLength / 2;

                std::wstring name(fileName, fileNameLen);
                if (name.length() >= 4) {
                    std::wstring ext = name.substr(name.length() - 4);
                    if (_wcsicmp(ext.c_str(), L".exe") == 0 ||
                        _wcsicmp(ext.c_str(), L".dll") == 0) {
                        
                        std::wstring safeDrive = drive;
                        std::wstring fullPath = GetFullPathFromFRN(hVolume, pRecord->FileReferenceNumber);
                        
                        if (pRecord->Reason & USN_REASON_FILE_CREATE) {
                            callback(0, safeDrive, fullPath);
                        }
                        if (pRecord->Reason & USN_REASON_DATA_OVERWRITE) {
                            callback(1, safeDrive, fullPath);
                        }
                        if (pRecord->Reason & USN_REASON_RENAME_NEW_NAME) {
                            callback(2, safeDrive, fullPath);
                        }
                    }
                }
            }

            if (pRecord->Usn > currentUsn) {
                currentUsn = pRecord->Usn;
            }

            recordAreaSize -= pRecord->RecordLength;
            pRecord = (USN_RECORD_V2*)((BYTE*)pRecord + pRecord->RecordLength);
        }

        if (bytesReturned > sizeof(DWORD64)) {
            currentUsn = lastUsn;
        }
    }

    CloseHandle(hVolume);
    return 0;
}