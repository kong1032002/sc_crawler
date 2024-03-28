from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
import pandas as pd

def predict(data):
    label_encoder = LabelEncoder()
    dataframe = pd.read_csv('./Dataset/type_1/Dataset_v1.9.csv')
    dataframe.dropna(inplace=True)
    dataframe.rename(columns=lambda x : x.lower(), inplace=True)

    dataframe['label'] = label_encoder.fit_transform(dataframe['label'])
    print(dataframe.shape)
    dataframe.head()
    x = dataframe.drop(columns=['id', 'label'], axis=1)
    y = dataframe['label']
    scaler = StandardScaler().fit(x)
    x = pd.DataFrame(scaler.transform(x))

    x_train,x_test, y_train, y_test = train_test_split(x, y, test_siz  e=0.2, random_state=42)

    x_train = pd.DataFrame(x_train)
    x_test = pd.DataFrame(x_test)
    y_train = pd.DataFrame(y_train)
    y_test = pd.DataFrame(y_test)
    xgboost_model = XGBClassifier(objective="binary:logistic", n_estimators=20, random_state=42, eval_metric=["auc", "error", "error@0.6"])
    xgboost_model.fit(x_train, y_train, eval_set=[(x_test, y_test)])
    return xgboost_model.predict_proba(data)