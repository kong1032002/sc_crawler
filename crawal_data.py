from libs.uniswap_graphql import *
from libs.data_parse import *
from libs.data_preprocession import *
import pandas as pd
import os

df = pd.read_csv('./Dataset/type_1/Dataset_v1.9.csv')
file_path = './Dataset/type_7days/Dataset_v1.9.csv'

try:
    # Đọc file CSV để kiểm tra
    processed_df = pd.read_csv(file_path)
    processed_ids = processed_df['id'].tolist()
except FileNotFoundError:
    processed_ids = []

# Kiểm tra xem file có chứa dữ liệu hay không để quyết định có thêm header hay không
header = not os.path.exists(file_path)

for i in range(df.shape[0]):
    id_value = df.iloc[i]['id']
    
    # Kiểm tra xem id đã được xử lý trước đó hay chưa
    if id_value not in processed_ids:
        print(id_value)
        result = preprocessing(early_predict=7, pair_id=id_value.strip())
        result['label'] = df.iloc[i]['Label']
        result['lp_avg'] = df.iloc[i]['lp_avg']
        result['lp_std'] = df.iloc[i]['lp_std']
        result['lp_creator_holding_ratio'] = df.iloc[i]['lp_creator_holding_ratio']
        result['lp_lock_ratio'] = df.iloc[i]['lp_lock_ratio']
        result['token_burn_ratio'] = df.iloc[i]['token_burn_ratio']
        result['token_creator_holding_ratio'] = df.iloc[i]['token_creator_holding_ratio']
        result['number_of_token_creation_of_creator'] = df.iloc[i]['number_of_token_creation_of_creator']
        # Ghi dữ liệu vào file CSV
        if(i>0):
            header = False
        pd.DataFrame([result]).to_csv(file_path, mode='a', header=header, index=False)
        processed_ids.append(id_value)

print("Data processing completed.")
