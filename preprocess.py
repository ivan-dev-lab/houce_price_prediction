import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np

## \brief Функция предобработки данных 
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param fpath Путь до необработанных данных
## \return Словарь dict с тремя ключами: все данные, признаки, целевые переменные
def preprocess (fpath: str) -> dict:
    pd.options.display.float_format = '{:.2f}'.format

    data = pd.read_csv(fpath)

    data.drop_duplicates(inplace=True)
    data["price"].replace(0, np.nan, inplace=True)
    data.dropna(inplace=True)

    data_preprocessed_dict = {
        "data": pd.DataFrame,
        "X": pd.DataFrame,
        "Y": pd.DataFrame,
    }
    
    data.drop("date", axis=1, inplace=True)
    data.drop("street", axis=1, inplace=True)
    data.drop("statezip", axis=1, inplace=True)
    data.drop("country", axis=1, inplace=True)
    data.drop("sqft_above", axis=1, inplace=True)

    data = pd.get_dummies(data, columns=["city"], prefix=["city"])
    data_columns = data.columns

    Y = data["price"]

    scaler = StandardScaler()
    data = pd.DataFrame(data=scaler.fit_transform(data), columns=data_columns)

    X = data[['bedrooms','bathrooms','sqft_living','sqft_lot']]


    data_preprocessed_dict["data"] = data
    data_preprocessed_dict["X"] = X
    data_preprocessed_dict["Y"] = Y

    return data_preprocessed_dict
    
preprocess("data/houses-data_kaggle.csv")