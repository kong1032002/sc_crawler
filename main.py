from libs.uniswap_graphql import *
from libs.data_parse import *
from libs.data_preprocession import *
import pandas as pd

df = pd.read_csv('./Dataset/type_1/Dataset_v1.9.csv').head()
result = preprocessing(early_predict=7,pair_id=df.iloc[0]['id'].strip())
print(json.dumps(result, indent=1))
# data = []
# for i in range(df.shape[0]):
#     print(df.iloc[i]['Label'])
#     result['Label'] = df.iloc[i]['Label']
#     data.append(result)
    
# data.to_csv('./Dataset/type_7days/Dataset_v1.9.csv')
# print(data)
