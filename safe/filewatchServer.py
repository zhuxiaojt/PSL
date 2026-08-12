import scanner
import threading
import delfile
import logger

from libs.pipe import PipeServer

def on_catch_file(file_path):
    result = scanner.check_file(file_path)
    if result == 'malicious':
        logger.log(f'[WATCHER] 发现威胁：{file_path}')
    elif result == 'suspicious':
        logger.log(f'[WATCHER] 发现可疑威胁：{file_path}')

def handler(read, write):
    data = read().decode('utf-8')
    print(data)
    if(data[:6] == 'catch_'):
        file_path = data[6:]
        thread = threading.Thread(target=on_catch_file, args=(file_path,),daemon=True)
        thread.start()

def server():
    server = PipeServer('PSL_SAFE_FILE_WATCH_SERVER')
    server.server(handler)
