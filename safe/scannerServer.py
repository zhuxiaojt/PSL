import scanner
import json
import threading
import delfile

from libs.pipe import PipeServer

def handler(read, write):
    data = read().decode('utf-8')
    print(data)
    if(data == 'fast_scan'):
        if(scanner.is_scanning):
            return
        thread = threading.Thread(target=scanner.fast_scan, daemon=True)
        thread.start()
    elif(data == 'disk_scan'):
        if(scanner.is_scanning):
           return
        thread = threading.Thread(target=scanner.disk_scan, daemon=True)
        thread.start()
    elif(data[:19] == 'custom_folder_scan_'):
        if(scanner.is_scanning):
            return
        path = data[19:]
        path = path.strip()
        thread = threading.Thread(target=scanner.custom_folder_scan, args=([path],), daemon=True)
        thread.start()
    elif(data == 'query_status'):
        print('get query_status')
        if (scanner.is_scanning):
            process = scanner.process
            scanning_file = scanner.scanning_file
            malicious_files = scanner.malicious_files
            suspicious_files = scanner.suspicious_files
            scanned_file_count = scanner.scanned_file_count
            status = {
                'status': 'scanning',
                'process': process,
                'scanning_file': scanning_file,
                'malicious_files': malicious_files,
                'suspicious_files': suspicious_files,
                'scanned_file_count': scanned_file_count
            }
            write(json.dumps(status).encode('utf-8'))
        elif (scanner.is_done):
            malicious_files = scanner.malicious_files
            suspicious_files = scanner.suspicious_files
            scanned_file_count = scanner.scanned_file_count
            doing_tasks = delfile.doing_tasks
            status = {
                'status': 'done',
                'malicious_files': malicious_files,
                'suspicious_files': suspicious_files,
                'scanned_file_count': scanned_file_count,
                'doing_quarantine': doing_tasks
            }
            write(json.dumps(status).encode('utf-8'))
        else:
            status = {
                'status': 'unstarted',
            }
            write(json.dumps(status).encode('utf-8'))
    elif(data == 'go_unstarted'):
        if(scanner.is_scanning):
            return
        scanner.is_done = False
    elif(data == 'quarantine_files'):
        thread = threading.Thread(target=scanner.quarantine_files, daemon=True)
        thread.start()
    elif(data[:16] == 'quarantine_file_'):
        file_path = data[16:]
        file_path = file_path.strip()
        thread = threading.Thread(target=delfile.quarantine_file, args=(file_path,), daemon=True)
        thread.start()
    elif(data[:24] == 'delete_quarantined_file_'):
        uuid = data[24:]
        uuid = uuid.strip()
        thread = threading.Thread(target=delfile.delete_quarantined_file, args=(uuid,), daemon=True)
        thread.start()
    elif(data[:25] == 'restore_quarantined_file_'):
        uuid = data[25:]
        uuid = uuid.strip()
        thread = threading.Thread(target=delfile.restore_quarantined_file, args=(uuid,), daemon=True)
        thread.start()
    elif(data == 'get_quarantined_files'):
        quarantined_files = delfile.get_quarantined_files_json()
        write(quarantined_files.encode('utf-8'))

def server():
    server = PipeServer('PSL_SAFE_SCANNER_SERVER')
    server.server(handler)
