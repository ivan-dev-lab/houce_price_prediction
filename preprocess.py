import pandas as pd
from sklearn.preprocessing import StandardScaler

## \brief Функция предобработки данных 
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param fpath Путь до необработанных данных
## \return Словарь dict с тремя ключами: все данные, признаки, целевые переменные
def preprocess (fpath: str) -> dict:
    pd.options.display.float_format = '{:.2f}'.format

    data = pd.read_csv(fpath)

    data_preprocessed_dict = {
        "data": pd.DataFrame,
        "X": pd.DataFrame,
        "Y": pd.DataFrame,
    }

    
    data.drop("date", axis=1, inplace=True)
    data.drop("street", axis=1, inplace=True)
    data.drop("statezip", axis=1, inplace=True)
    data.drop("country", axis=1, inplace=True)
    data.drop("sqft_basement", axis=1, inplace=True)

    city_replacements = {}

    for unique_index,unique_city in enumerate(data["city"].unique()):
        city_replacements[unique_city] = unique_index

    data["city"].replace(city_replacements, inplace=True)
    data_columns = data.columns

    Y = data["price"]

    scaler = StandardScaler().fit(data)
    data = pd.DataFrame(data=scaler.transform(data), columns=data_columns)

    X = data.iloc[:, 1:]

    data_preprocessed_dict["data"] = data
    data_preprocessed_dict["X"] = X
    data_preprocessed_dict["Y"] = Y

    print(data_preprocessed_dict)

    return data_preprocessed_dict
    
