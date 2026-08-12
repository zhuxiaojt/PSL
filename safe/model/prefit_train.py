from sklearn.ensemble import RandomForestClassifier
import pandas
import sys
import os
import joblib

data_path = sys.argv[1]
data_csv = os.path.join(data_path, 'fit_data.csv')

if not os.path.exists(data_csv):
    print('数据文件不存在')
    sys.exit(1)

df = pandas.read_csv(data_csv)
X = df.drop(columns=['label'])
Y = df['label']

model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
model.fit(X, Y)
joblib.dump(model, os.path.join(data_path, 'prefit_model.pkl'))
print(f'模型训练完成，已保存为{os.path.join(data_path, "prefit_model.pkl")}')
