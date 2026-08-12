import joblib
import sys
import os
import pandas
import win32api
import delfile
from libs.getfeat import getfeat, FEAT_HEADER
from configManager import getConfigContentDict
import logger

prefit_model = joblib.load(os.path.join(
    os.path.dirname(__file__), 'model', 'prefit_model.pkl'))

is_scanning = False
is_done = False
scanning_file = None
malicious_files = []
suspicious_files = []
process = 0
scanned_file_count = 0

config = getConfigContentDict()

def check_file_use_model(file_path, model):
    feat = getfeat(file_path)
    if (feat):
        pdf = pandas.DataFrame([feat], columns=FEAT_HEADER)
        result = model.predict_proba(pdf)[0][1]
        return result
    else:
        return None


def check_file(file_path):
    result = check_file_use_model(file_path, prefit_model)
    if (result is None):
        return 'unknown'
    elif (result > 0.7):
        return 'malicious'
    elif (result > 0.65):
        return 'suspicious'
    else:
        return 'safe'


def fast_scan():
    user_profile = os.path.expanduser("~")
    targets = [
        os.path.join(user_profile, "Downloads"),
        os.path.join(user_profile, "Desktop"),
        os.path.join(user_profile, "AppData", "Local", "Temp")
    ]
    return custom_folder_scan(targets)


def disk_scan():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return custom_folder_scan(drives)


def custom_folder_scan(folder_paths, is_root=True, allocation_process=100, base_process=0):
    global is_scanning, is_done, scanning_file, malicious_files, suspicious_files, process, scanned_file_count, config
    process=base_process
    if (is_root):
        config = getConfigContentDict()
        is_scanning = True
        is_done = False
        scanning_file = None
        malicious_files = []
        suspicious_files = []
        scanned_file_count = 0
        logger.log(f'[SCANNER] 开始扫描：{folder_paths}')
    if (len(folder_paths) == 1):
        try:
            files = os.listdir(folder_paths[0])
        except:
            return malicious_files, suspicious_files
        file_count = len([1 for file in files if os.path.isfile(
            os.path.join(folder_paths[0], file))])
        folder_count = len(files) - file_count
        done_file_count = 0
        give_process = allocation_process // (folder_count + 1)
        file_paths = [os.path.join(folder_paths[0], file) for file in files]
        for file_path in file_paths:
            if (os.path.isfile(file_path)):
                if (file_path.endswith('.exe') or file_path.endswith('.dll')):
                    scanning_file = file_path
                    result = check_file(file_path)
                    scanned_file_count += 1
                    if (result == 'malicious'):
                        malicious_files.append(file_path)
                    elif (result == 'suspicious' and config.get('reportSuspiciousFiles', True)):
                        suspicious_files.append(file_path)
                done_file_count += 1
                if (done_file_count == file_count):
                    process += give_process
            else:
                custom_folder_scan(
                    [file_path], is_root=False, allocation_process=give_process, base_process=process)
        process = base_process + allocation_process
        if (is_root):
            is_scanning = False
            is_done = True
            logger.log(f'[SCANNER] 扫描完成：{folder_paths}')
        return malicious_files, suspicious_files
    else:
        give_process = allocation_process // len(folder_paths)
        for folder_path in folder_paths:
            custom_folder_scan([folder_path], is_root=False,
                               allocation_process=give_process, base_process=process)
        process = base_process + allocation_process
        if (is_root):
            is_scanning = False
            is_done = True
            logger.log(f'[SCANNER] 扫描完成：{folder_paths}')
        return malicious_files, suspicious_files


def custom_file_scan(file_paths):
    global is_scanning, is_done, scanning_file, malicious_files, suspicious_files
    is_scanning = True
    is_done = False
    scanning_file = None
    malicious_files = []
    suspicious_files = []
    for file_path in file_paths:
        scanning_file = file_path
        result = check_file(file_path)
        if (result == 'malicious'):
            malicious_files.append(file_path)
        elif (result == 'suspicious'):
            suspicious_files.append(file_path)

    return malicious_files, suspicious_files

def quarantine_files():
    global is_done
    if is_done:
        logger.log('[SCANNER] 开始隔离威胁')
        for file_path in malicious_files:
            delfile.quarantine_file(file_path)
        for file_path in suspicious_files:
            delfile.quarantine_file(file_path)
        malicious_files.clear()
        suspicious_files.clear()
        is_done = False
        logger.log('[SCANNER] 隔离完成')