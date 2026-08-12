import pefile
import os
import math

SENSITIVE_API_MAP = {
    "CreateRemoteThread": 0,
    "WriteProcessMemory": 1,
    "VirtualAllocEx": 2,
    "OpenProcess": 3,
    "NtCreateThreadEx": 4,
    "QueueUserAPC": 5,
    "RegSetValueExA": 6,
    "RegOpenKeyExA": 7,
    "RegCreateKeyExA": 8,
    "ShellExecuteA": 9,
    "URLDownloadToFileA": 10,
    "WinHttpOpen": 11,
    "InternetOpenUrlA": 12,
    "WSAStartup": 13,
    "connect": 14,
    "send": 15,
    "recv": 16,
    "CryptEncrypt": 17,
    "CryptDecrypt": 18,
    "AdjustTokenPrivileges": 19,
    "NtQueryInformationProcess": 20,
    "NtSetInformationProcess": 21,
    "ReadProcessMemory": 22,
    "EnumProcesses": 23,
    "RegDeleteKeyA": 24,
    "RegDeleteValueA": 25,
    "RegQueryValueExA": 26,
    "CryptAcquireContextA": 27,
    "DeleteFileA": 28,
    "MoveFileA": 29,
    "CopyFileA": 30,
    "SetTokenInformation": 31,
    "NtSetInformationThread": 32,
    "WinExec": 33,
    "CreateProcessA": 34,
    "SchTasks": 35,
    "NetScheduleJobAdd": 36,
    "CreateServiceA": 37,
    "StartServiceA": 38,
    "OpenSCManagerA": 39
}
API_VECTOR_SIZE = len(SENSITIVE_API_MAP)
FEAT_HEADER = [
    'file_size_log2',
    'size_of_image_log2', 
    'num_sections', 
    'is_dll', 
    'imports_count', 
    'entropy', 
    'resource_entries', 
    'export_function_count', 
    'code_section_writable',
     *[f'api_{i}' for i in range(API_VECTOR_SIZE)]
]
def getfeat(file_path):
    try:
        pe = pefile.PE(file_path)
        file_size = max(os.path.getsize(file_path), 1)
        file_size_log2 = math.log2(file_size)
        size_of_image = max(pe.OPTIONAL_HEADER.SizeOfImage, 1)
        size_of_image_log2 = math.log2(size_of_image)
        num_sections = pe.FILE_HEADER.NumberOfSections
        is_dll = 1 if pe.FILE_HEADER.Characteristics & 0x2000 else 0
        imports_count = 0
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            imports_count = len(pe.DIRECTORY_ENTRY_IMPORT)
        api_feature_vector = [0] * API_VECTOR_SIZE
        entropy = 0.0
        for section in pe.sections:
            if b'.text' in section.Name or b'CODE' in section.Name:
                entropy = section.get_entropy()
                break
        has_resources = 1 if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE') else 0
        resource_entries = 0
        if has_resources:
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                resource_entries += 1
        has_export_table = 1 if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0
        export_function_count = len(pe.DIRECTORY_ENTRY_EXPORT.symbols) if has_export_table else 0
        code_section_writable = 0
        for section in pe.sections:
            if b'.text' in section.Name:
                if section.Characteristics & 0x80000000:
                    code_section_writable = 1
                break
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        api_name = imp.name.decode('utf-8')
                        if api_name in SENSITIVE_API_MAP:
                            api_feature_vector[SENSITIVE_API_MAP[api_name]] = 1
        pe.close()
        return [
            file_size_log2,
            size_of_image_log2,
            num_sections,
            is_dll,
            imports_count,
            entropy,
            resource_entries,
            export_function_count,
            code_section_writable,
            *api_feature_vector
        ]
    except:
        return None
