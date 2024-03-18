from libs.uniswap_graphql import *
from libs.data_parse import *
from libs.data_preprocession import *
import pandas as pd

df = pd.read_csv('./Dataset/type_1/Dataset_v1.9.csv')
file_path = './Dataset/type_7days/Dataset_v1.9.csv'

try:
    # Đọc file CSV để kiểm tra
    processed_df = pd.read_csv(file_path)
    processed_ids = processed_df['id'].tolist()
except FileNotFoundError:
    processed_ids = []

for i in range(df.shape[0]):
    id_value = df.iloc[i]['id']
    
    # Kiểm tra xem id đã được xử lý trước đó hay chưa
    if id_value not in processed_ids:
        print(id_value)
        result = preprocessing(early_predict=7, pair_id=id_value.strip())
        result['Label'] = df.iloc[i]['Label']
        
        # Ghi dữ liệu vào file CSV
        pd.DataFrame([result]).to_csv(file_path, mode='a', header=False, index=False)
        processed_ids.append(id_value)

print("Data processing completed.")
