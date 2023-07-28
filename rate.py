from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
import pandas as pd
import numpy as np

data_raw = pd.read_csv("data/houses-data_raw.csv", index_col=[0])

replacements = {
    "индивидуальное жилищное строительство": 1,
    "садоводство": 0,
    "кирпич": 1,
    "дерево": 2,
    "блок": 3,
    "монолит-кирпич": 4,
    "монолит": 5,
}

X = data_raw.replace(replacements).iloc[:, 1:]


def rate_scalers (scalers: dict, X: pd.DataFrame) -> dict:
    result = {}
    intermediate_score_scaler = []

    for key in scalers.keys():
        result[key] = []

    for name, scaler in scalers.items():
        
        intermediate_score_scaler = []

        working_scaler = scaler().fit(X)
        intermediate_X = pd.DataFrame(data=working_scaler.transform(X), columns=X.columns)

        for column in intermediate_X.columns:
            intermediate_score_scaler.append({f"min[{column}]": min(intermediate_X[column]), f"max[{column}]": max(intermediate_X[column])})
        
        score_scaler = result[name].copy()
        score_scaler.append({"MIN_MAX": intermediate_score_scaler})
        result[name] = score_scaler.copy()

        intermediate_score_scaler = []
        score_scaler = []

        for column in intermediate_X.columns:
            intermediate_score_scaler.append({f"mean[{column}]": np.mean(intermediate_X[column]), f"std[{column}]": np.std(intermediate_X[column])})

        score_scaler = result[name].copy()
        score_scaler.append({"MEAN_STD": intermediate_score_scaler})
        result[name] = score_scaler.copy()

        intermediate_score_scaler = []
        score_scaler = []

    return result


scalers = {
    "MinMaxScaler": MinMaxScaler,
    "StandardScaler": StandardScaler,
    "MaxAbsScaler": MaxAbsScaler, 
    "RobustScaler": RobustScaler,
}

score_scalers = rate_scalers(scalers, X=X)