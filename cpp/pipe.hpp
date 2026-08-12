#pragma once
#include <windows.h>
#include <string>
#include <functional>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <queue>

class PipeClient {
private:
    std::wstring pipeName;
    HANDLE handle;
    std::atomic<bool> connected;
    std::atomic<bool> running;
    
    std::queue<std::string> dataQueue;
    std::mutex queueMutex;
    std::condition_variable queueCv;
    
    std::thread readThread;
    std::atomic<bool> hasPendingRead;
    std::function<void()> onDataCallback;
    
    std::wstring toWide(const std::string& str) {
        int len = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, NULL, 0);
        std::wstring wstr(len, L'\0');
        MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, &wstr[0], len);
        return wstr;
    }

    void readLoop() {
        char buffer[65536];
        while (running && connected) {
            DWORD bytesRead = 0;
            if (ReadFile(handle, buffer, sizeof(buffer) - 1, &bytesRead, NULL) && bytesRead > 0) {
                buffer[bytesRead] = '\0';
                std::string data(buffer, bytesRead);
                
                {
                    std::lock_guard<std::mutex> lock(queueMutex);
                    dataQueue.push(data);
                }
                queueCv.notify_one();
                
                if (onDataCallback) {
                    onDataCallback();
                }
            } else {
                DWORD err = GetLastError();
                if (err == ERROR_BROKEN_PIPE || err == ERROR_NO_DATA) {
                    connected = false;
                    break;
                }
                Sleep(10);
            }
        }
    }

public:
    explicit PipeClient(const std::string& name) 
        : handle(INVALID_HANDLE_VALUE), connected(false), running(false), hasPendingRead(false) {
        pipeName = L"\\\\.\\pipe\\" + toWide(name);
    }

    ~PipeClient() {
        disconnect();
    }

    bool connect(std::function<void(std::function<std::string()>, 
                                    std::function<void(const std::string&)>, 
                                    std::function<void()>)> handler) {
        for (int retry = 0; retry < 20; retry++) {
            handle = CreateFileW(
                pipeName.c_str(),
                GENERIC_READ | GENERIC_WRITE,
                0,
                NULL,
                OPEN_EXISTING,
                0,
                NULL
            );

            if (handle != INVALID_HANDLE_VALUE) {
                connected = true;
                running = true;
                break;
            }

            DWORD err = GetLastError();
            if (err == ERROR_PIPE_BUSY || err == ERROR_FILE_NOT_FOUND) {
                Sleep(50 * (retry + 1));
                continue;
            }
            return false;
        }

        if (!connected) return false;

        readThread = std::thread(&PipeClient::readLoop, this);

        auto read = [this]() -> std::string {
            std::unique_lock<std::mutex> lock(queueMutex);
            queueCv.wait(lock, [this] { return !dataQueue.empty() || !running; });
            
            if (dataQueue.empty()) {
                return "";
            }
            
            std::string data = dataQueue.front();
            dataQueue.pop();
            return data;
        };

        auto write = [this](const std::string& data) {
            if (!connected || handle == INVALID_HANDLE_VALUE) return;
            DWORD written = 0;
            WriteFile(handle, data.c_str(), data.size(), &written, NULL);
        };

        auto disconnect = [this]() {
            this->disconnect();
        };

        handler(read, write, disconnect);

        return true;
    }

    bool connect() {
        for (int retry = 0; retry < 20; retry++) {
            handle = CreateFileW(
                pipeName.c_str(),
                GENERIC_READ | GENERIC_WRITE,
                0,
                NULL,
                OPEN_EXISTING,
                0,
                NULL
            );

            if (handle != INVALID_HANDLE_VALUE) {
                connected = true;
                running = true;
                readThread = std::thread(&PipeClient::readLoop, this);
                return true;
            }

            DWORD err = GetLastError();
            if (err == ERROR_PIPE_BUSY || err == ERROR_FILE_NOT_FOUND) {
                Sleep(50 * (retry + 1));
                continue;
            }
            return false;
        }
        return false;
    }

    std::string read() {
        std::unique_lock<std::mutex> lock(queueMutex);
        queueCv.wait(lock, [this] { return !dataQueue.empty() || !running; });
        if (dataQueue.empty()) return "";
        std::string data = dataQueue.front();
        dataQueue.pop();
        return data;
    }

    bool write(const std::string& data) {
        if (!connected || handle == INVALID_HANDLE_VALUE) return false;
        DWORD written = 0;
        return WriteFile(handle, data.c_str(), data.size(), &written, NULL) != 0;
    }

    void disconnect() {
        running = false;
        connected = false;
        
        queueCv.notify_all();
        
        if (readThread.joinable()) {
            readThread.join();
        }
        
        if (handle != INVALID_HANDLE_VALUE) {
            CloseHandle(handle);
            handle = INVALID_HANDLE_VALUE;
        }
        
        std::lock_guard<std::mutex> lock(queueMutex);
        while (!dataQueue.empty()) dataQueue.pop();
    }

    bool isConnected() const { return connected; }
};