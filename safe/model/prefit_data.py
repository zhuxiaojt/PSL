import sys
import os
import csv
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.join(current_dir, '..', 'libs')

if target_dir not in sys.path:
    sys.path.insert(0, target_dir)

from getfeat import getfeat, FEAT_HEADER

data_path = sys.argv[1]
# 格式：
# data_path/
#   +/
#       安全样本.exe
#       安全样本.dll
#       ...
#   -/
#       恶意样本.exe
#       恶意样本.dll
#       ...
safe_feat_list = []
bad_feat_list = []
if os.path.exists(data_path):
    safe_dir = os.path.join(data_path, '+')
    bad_dir = os.path.join(data_path, '-')
    if os.path.exists(safe_dir) and os.path.exists(bad_dir):
        safe_files = os.listdir(safe_dir)
        bad_files = os.listdir(bad_dir)
        for file in safe_files:
            if file.endswith('.exe') or file.endswith('.dll'):
                feat = getfeat(os.path.join(safe_dir, file))
                if(feat):
                    safe_feat_list.append(feat)
        for file in bad_files:
            if file.endswith('.exe') or file.endswith('.dll'):
                feat = getfeat(os.path.join(bad_dir, file))
                if(feat):
                    bad_feat_list.append(feat)
    else:
        print('数据路径格式错误')
        sys.exit(1)
else:
    print('数据路径不存在')
    sys.exit(1)

with open(os.path.join(data_path, 'fit_data.csv'), 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    headers = FEAT_HEADER + ['label']
    writer.writerow(headers)
    rows = []
    for feat in safe_feat_list:
        feat.append(0)
        rows.append(feat)
    for feat in bad_feat_list:
        feat.append(1)
        rows.append(feat)
    random.shuffle(rows)
    for row in rows:
        writer.writerow(row)
    print(f'数据处理完成，已保存到 {os.path.join(data_path, "fit_data.csv")}，共 {len(rows)} 条数据')
