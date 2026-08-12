import win32pipe, win32file, pywintypes

class PipeServer:
    def __init__(self, pipe_name: str):
        self.pipe_name = f'\\\\.\\pipe\\{pipe_name}'
        self.pipe = win32pipe.CreateNamedPipe(
            self.pipe_name,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,  # ← 改这里
            1, 65536, 65536, 0, None
        )
    
    def server(self, handler):
        def write(data):
            win32file.WriteFile(self.pipe, data)
            win32file.FlushFileBuffers(self.pipe)
        def read():
            result, data = win32file.ReadFile(self.pipe, 65536)
            return data
        while True:
            try:
                win32pipe.ConnectNamedPipe(self.pipe, None)
                handler(read=read, write=write)
            except pywintypes.error as e:
                if e.winerror == 232:
                    if self.pipe:
                        try:
                            win32file.CloseHandle(self.pipe)
                        except:
                            pass
                    self.pipe = win32pipe.CreateNamedPipe(
                        self.pipe_name,
                        win32pipe.PIPE_ACCESS_DUPLEX,
                        win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
                        1, 65536, 65536, 0, None
                    )
                else:
                    print(e)
    
    def close(self):
        win32file.CloseHandle(self.pipe)
