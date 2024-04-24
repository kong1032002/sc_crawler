import json
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
import pandas as pd
import joblib
import os


label_encoder = LabelEncoder()
fast_predict_df = pd.read_csv('./Dataset/type_7days/Dataset_v1.9.csv')
fast_predict_df.dropna(inplace=True) 
fast_predict_df.rename(columns=lambda x : x.lower(), inplace=True)
fast_predict_df['label'] = label_encoder.fit_transform(fast_predict_df['label'])
x_fast = fast_predict_df.drop(columns=['id', 'label', 'number_of_token_creation_of_creator', 'token_creator_holding_ratio', 'lp_lock_ratio', 'lp_creator_holding_ratio'], axis=1)
scaler = StandardScaler().fit(x_fast)

model_file = './models/fast_predict.pkl'

# Training model
if os.path.exists(model_file):
    # Load mô hình từ tệp đã tồn tại
    fast_predict_model = joblib.load(model_file)
    print("Model đã được tải từ tệp đã tồn tại.")
else:
    # Huấn luyện mô hình
    x_fast = pd.DataFrame(scaler.transform(x_fast))
    y = fast_predict_df['label']
    
    fast_predict_model = XGBClassifier(objective="binary:logistic", n_estimators=100, random_state=42)
    fast_predict_model.fit(x_fast, y)
    
    # Lưu mô hình
    joblib.dump(fast_predict_model, model_file)
    print("Model đã được huấn luyện và lưu vào tệp.")

def fast_predict(data):

    # Chuyển đổi dữ liệu bản ghi thành DataFrame
    data_df = pd.DataFrame(data)  

    # Preprocess and predict data
    data_df.rename(columns=lambda x: x.lower(), inplace=True)
    data_df = data_df.drop(columns=['id', 'label', 'token_creator_holding_ratio', 'lp_lock_ratio', 'lp_creator_holding_ratio'], axis=1)
    data_df = pd.DataFrame(scaler.transform(data_df))

    # Predict probabilities
    probabilities = fast_predict_model.predict_proba(data_df)
    is_rugpull = fast_predict_model.predict(data_df)
    # Print probabilities of being 0 and 1
    print(f"Fast predict: Probability of being rugpull: {probabilities[0][1] * 100} %" )  # Chuyển đổi thành phần trăm
    # Return predicted probabilities
    return (probabilities, is_rugpull)

def normal_predict(data):
    data_df = pd.DataFrame([data])  # Chuyển đổi dữ liệu bản ghi thành DataFrame
    # Preprocess and predict data
    data_df.rename(columns=lambda x: x.lower(), inplace=True)
    data_df = data_df.drop(columns=['id', 'label', 'number_of_token_creation_of_creator', 'token_creator_holding_ratio', 'lp_lock_ratio', 'lp_creator_holding_ratio'], axis=1)
    data_df = pd.DataFrame(scaler.transform(data_df))

    return 1
