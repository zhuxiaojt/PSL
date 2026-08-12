from libs.pipe import PipeServer
from configManager import getConfigContentDict, getAppDataPath
import os

logs = []
config = getConfigContentDict()
appdata_path = getAppDataPath()

def log(text):
    logs.append(text)
    with open(os.path.join(appdata_path, 'log.txt'), 'a', encoding='utf-8') as f:
        f.write(text + '\n')
    while len(logs) > config.get('maxLogs', 100):
        logs.pop(0)

def clearLogs():
    logs.clear()
    log('[LOGGER] 日志已清除')

def clearLogFile():
    with open(os.path.join(appdata_path, 'log.txt'), 'w', encoding='utf-8') as f:
        f.write('')
    clearLogs()

def reloadConfig():
    global config
    config = getConfigContentDict()

def handler(read, write):
    data = read().decode('utf-8')
    print(data)
    if(data == 'get_logs'):
        write('\n'.join(logs).encode('utf-8'))
    elif(data == 'clear_logs'):
        clearLogs()
    elif(data == 'clear_log_file'):
        clearLogFile()

def server():
    server = PipeServer('PSL_SAFE_LOGGER_SERVER')
    server.server(handler)