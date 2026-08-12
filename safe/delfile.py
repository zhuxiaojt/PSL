import psutil
import os
import uuid
import json
from configManager import getAppDataPath
import scanner
import logger

appdata_path = getAppDataPath()
doing_tasks = []

def kill_process_using_file(file_path):
    nowpid = os.getpid()
    for proc in psutil.process_iter():
        if proc.pid == nowpid:
            continue
        try:
            files = proc.open_files()
            for f in files:
                try:
                    if os.path.samefile(f.path, file_path):
                        proc.kill()
                        logger.log(f'[DELFILE] 已终止占用文件 {file_path} 的进程 {proc.pid}')
                except (FileNotFoundError, OSError):
                    pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def delete_file(file_path):
    global doing_tasks
    doing_tasks.append(('delete_file', file_path))
    logger.log(f'[DELFILE] 删除文件：{file_path}')
    if not os.path.exists(file_path):
        logger.log(f'[DELFILE] 删除文件失败（文件不存在）：{file_path}')
        return False
    try:
        os.remove(file_path)
        if file_path in scanner.malicious_files:
            scanner.malicious_files.remove(file_path)
        if file_path in scanner.suspicious_files:
            scanner.suspicious_files.remove(file_path)
        doing_tasks.remove(('delete_file', file_path))
        logger.log(f'[DELFILE] 删除文件成功：{file_path}')
        return True
    except:
        kill_process_using_file(file_path)
        try:
            os.remove(file_path)
            if file_path in scanner.malicious_files:
                scanner.malicious_files.remove(file_path)
            if file_path in scanner.suspicious_files:
                scanner.suspicious_files.remove(file_path)
            doing_tasks.remove(('delete_file', file_path))
            logger.log(f'[DELFILE] 删除文件成功：{file_path}')
            return True
        except:
            logger.log(f'[DELFILE] 删除文件失败：{file_path}')
            return False

def quarantine_file(file_path):
    global doing_tasks
    doing_tasks.append(('quarantine_file', file_path))
    logger.log(f'[DELFILE] 隔离文件：{file_path}')
    if not os.path.exists(file_path):
        logger.log(f'[DELFILE] 隔离文件失败（文件不存在）：{file_path}')
        return False
    try:
        if not os.path.exists(os.path.join(appdata_path, 'quarantines')):
            os.makedirs(os.path.join(appdata_path, 'quarantines'), exist_ok=True)
        uuid_str = str(uuid.uuid4())
        os.rename(file_path, os.path.join(appdata_path, 'quarantines', uuid_str + ".quarantine"))
        if not os.path.exists(os.path.join(appdata_path, 'quarantines', 'index.json')):
            with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'w') as f:
                f.write("{}")
        with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'r') as f:
            index = json.load(f)
        index[uuid_str] = file_path
        with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'w') as f:
            json.dump(index, f, ensure_ascii=False)
        if file_path in scanner.malicious_files:
            scanner.malicious_files.remove(file_path)
        if file_path in scanner.suspicious_files:
            scanner.suspicious_files.remove(file_path)
        doing_tasks.remove(('quarantine_file', file_path))
        logger.log(f'[DELFILE] 隔离文件成功：{file_path}')
        return True
    except:
        kill_process_using_file(file_path)
        try:
            if not os.path.exists(os.path.join(appdata_path, 'quarantines')):
                os.makedirs(os.path.join(appdata_path, 'quarantines'), exist_ok=True)
            uuid_str = str(uuid.uuid4())
            os.rename(file_path, os.path.join(appdata_path, 'quarantines', uuid_str + ".quarantine"))
            if not os.path.exists(os.path.join(appdata_path, 'quarantines', 'index.json')):
                with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'w') as f:
                    f.write("{}")
            with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'r') as f:
                index = json.load(f)
            index[uuid_str] = file_path
            with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'w') as f:
                json.dump(index, f, ensure_ascii=False)
            if file_path in scanner.malicious_files:
                scanner.malicious_files.remove(file_path)
            if file_path in scanner.suspicious_files:
                scanner.suspicious_files.remove(file_path)
            doing_tasks.remove(('quarantine_file', file_path))
            logger.log(f'[DELFILE] 隔离文件成功：{file_path}')
            return True
        except:
            logger.log(f'[DELFILE] 隔离文件失败：{file_path}')
            return False
def delete_quarantined_file(uuid_str):
    global doing_tasks
    doing_tasks.append(('delete_quarantined_file', uuid_str))
    logger.log(f'[DELFILE] 删除已隔离文件：{uuid_str}')
    if not os.path.exists(os.path.join(appdata_path, 'quarantines')):
        logger.log(f'[DELFILE] 删除已隔离文件失败（隔离目录不存在）：{uuid_str}')
        return False
    if not os.path.exists(os.path.join(appdata_path, 'quarantines', 'index.json')):
        logger.log(f'[DELFILE] 删除已隔离文件失败（隔离区索引文件不存在）：{uuid_str}')
        return False
    with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'r') as f:
        index = json.load(f)
    if uuid_str not in index:
        logger.log(f'[DELFILE] 删除已隔离文件失败（文件不存在）：{uuid_str}')
        return False
    delete_file(os.path.join(appdata_path, 'quarantines', uuid_str + ".quarantine"))
    del index[uuid_str]
    with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'w') as f:
        json.dump(index, f, ensure_ascii=False)
    doing_tasks.remove(('delete_quarantined_file', uuid_str))
    logger.log(f'[DELFILE] 删除已隔离文件成功：{uuid_str}')
    return True
    
def restore_quarantined_file(uuid_str, overwrite=False):
    global doing_tasks
    doing_tasks.append(('restore_quarantined_file', uuid_str))
    logger.log(f'[DELFILE] 恢复已隔离文件：{uuid_str}')
    print('restore')
    if not os.path.exists(os.path.join(appdata_path, 'quarantines')):
        logger.log(f'[DELFILE] 恢复已隔离文件失败（隔离目录不存在）：{uuid_str}')
        return False
    if not os.path.exists(os.path.join(appdata_path, 'quarantines', 'index.json')):
        logger.log(f'[DELFILE] 恢复已隔离文件失败（隔离区索引文件不存在）：{uuid_str}')
        return False
    with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'r') as f:
        index = json.load(f)
    if uuid_str not in index:
        logger.log(f'[DELFILE] 恢复已隔离文件失败（文件不存在）：{uuid_str}')
        return False
    file_path = index[uuid_str]
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.exists(file_path):
        if not overwrite:
            logger.log(f'[DELFILE] 恢复已隔离文件失败（原目录存在文件）：{uuid_str}')
            return False
        else:
            if not delete_file(file_path):
                logger.log(f'[DELFILE] 恢复已隔离文件失败（无法删除原目录文件）：{uuid_str}')
                return False
    os.rename(os.path.join(appdata_path, 'quarantines', uuid_str + ".quarantine"), file_path)
    del index[uuid_str]
    with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'w') as f:
        json.dump(index, f, ensure_ascii=False)
    doing_tasks.remove(('restore_quarantined_file', uuid_str))
    logger.log(f'[DELFILE] 恢复已隔离文件成功：{uuid_str}')
    return True

def get_quarantined_files():
    if not os.path.exists(os.path.join(appdata_path, 'quarantines')):
        return {}
    if not os.path.exists(os.path.join(appdata_path, 'quarantines', 'index.json')):
        return {}
    with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'r') as f:
        index = json.load(f)
    return index

def get_quarantined_files_json():
    print("get_quarantined_files_json")
    if not os.path.exists(os.path.join(appdata_path, 'quarantines')):
        return '{}'
    if not os.path.exists(os.path.join(appdata_path, 'quarantines', 'index.json')):
        return '{}'
    with open(os.path.join(appdata_path, 'quarantines', 'index.json'), 'r') as f:
        index = f.read()
    return index