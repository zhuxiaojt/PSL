import appdirs
import os
import json
from libs.pipe import PipeServer
import subprocess

def getAppDataPath():
    config_dir=appdirs.user_data_dir("PSL Safe")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def getConfigFilePath():
    config_dir=getAppDataPath()
    config_file=os.path.join(config_dir,"config.json")
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write("{}")
    return config_file

def getConfigContentDict():
    config_file=getConfigFilePath()
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def getConfigContentJson():
    config_file=getConfigFilePath()
    with open(config_file, 'r') as f:
        config = f.read()
    return config

def saveConfigContentJson(config):
    import logger
    old_config = getConfigContentDict()
    with open(getConfigFilePath(), 'w') as f:
        f.write(config)
    new_config = getConfigContentDict()
    logger.log('[CONFIG] 已保存设置')

    old_enable_defendnot = old_config.get('enableDefendnot', False)
    new_enable_defendnot = new_config.get('enableDefendnot', False)
    if(new_enable_defendnot != old_enable_defendnot):
        defendnot_cwd = os.path.join(os.path.dirname(__file__),'defendnot')
        if(new_enable_defendnot):
            print("enable defendnot")
            subprocess.run(['cmd', '/c', os.path.join(defendnot_cwd, 'enable.bat')], check=True, cwd=defendnot_cwd)
        else:
            print("disable defendnot")
            subprocess.run(['cmd', '/c', os.path.join(defendnot_cwd, 'disable.bat')], check=True, cwd=defendnot_cwd)
    
    old_max_logs = old_config.get('maxLogs', 100)
    new_max_logs = new_config.get('maxLogs', 100)
    if(old_max_logs != new_max_logs):
        logger.reloadConfig()

def saveConfigContentDict(config):
    saveConfigContentJson(json.dumps(config, ensure_ascii=False))

def handler(read, write):
    data = read().decode('utf-8')
    if(data == 'get_config'):
        config = getConfigContentJson()
        write(config.encode('utf-8'))
    elif(data[:12] == 'save_config_'):
        config = data[12:]
        saveConfigContentJson(config)

def server():
    server = PipeServer('PSL_SAFE_CONFIG_SERVER')
    server.server(handler)
