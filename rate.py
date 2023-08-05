import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from preprocess import preprocess
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor, BaggingRegressor, AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression


# Оценка скалеров
def rate_scalers (scalers: dict, X: pd.DataFrame) -> dict:
    result = {}
    intermediate_score_scaler = []

    for name in scalers.keys():
        result[name] = []

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

def plot_scaler_data (scaler_score: dict, data_type: str, scaler_name: str, X: pd.DataFrame, fchart: str="scalers_charts/"):
    DATA = scaler_score[data_type]

    chart_data_full = []
    chart_data_1 = []
    chart_data_2 = []

    for index,column in enumerate(X.columns):
        chart_data_1.append(DATA[index][f"{data_type.lower().split('_')[0]}[{column}]"])
        chart_data_2.append(DATA[index][f"{data_type.lower().split('_')[1]}[{column}]"])

    chart_data_full.append(chart_data_1)
    chart_data_full.append(chart_data_2)

    chart_data_1 = []
    chart_data_2 = []
    
    sns.set_style("darkgrid")

    plt.figure(figsize=(10, 6))

    for i, data_row in enumerate(chart_data_full):
        plt.barh(X.columns, data_row, label=f"{data_type.lower().split('_')[i]}", alpha=0.5)   

    plt.xlabel("Признаки")
    plt.ylabel("Значения")
    plt.title(f"{data_type} - {scaler_name}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{fchart}/{data_type} - {scaler_name}")

def create_scaler_charts (score_scalers: dict, X: pd.DataFrame):
    for scaler_name, scaler_score_data in score_scalers.items():
        for scaler_score in scaler_score_data:
            if "MIN_MAX" in scaler_score:
                plot_scaler_data(scaler_score, "MIN_MAX", scaler_name, X)
            else:
                plot_scaler_data(scaler_score, "MEAN_STD", scaler_name, X)



models = {
    'LinearRegression': LinearRegression,
    'HistGradientBoostingRegressor': HistGradientBoostingRegressor,
    'ExtraTreesRegressor': ExtraTreesRegressor,
    'BaggingRegressor': BaggingRegressor,
    'AdaBoostRegressor': AdaBoostRegressor,
    'RandomForestRegressor': RandomForestRegressor,
    'GradientBoostingRegressor': GradientBoostingRegressor,
    'DecisionTreeRegressor': DecisionTreeRegressor
}

data_preprocessed_dict = preprocess("data/houses-data_raw.csv")

X = data_preprocessed_dict["X"]
Y = data_preprocessed_dict["Y"]


def rate_models (models: dict, X: pd.DataFrame, Y: pd.DataFrame, verbose=True) -> tuple:
    names, mse_scores, mae_scores, r2_scores = [], [], [], []

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    for name, Model in models.items():

        model = Model().fit(x_train, y_train)
        y_pred = model.predict(x_test)

        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        names.append(name)
        mse_scores.append(mse)
        mae_scores.append(mae)
        r2_scores.append(r2)

        if verbose:
            print(f"{name}:\nmean_squared_error: {mse}\nmean_absolute_error: {mae}\nr2_score: {r2}", end="\n\n")
    
    return (names, mse_scores, mae_scores, r2_scores)
     

def create_models_charts (models_rating: tuple) -> None:
    names, mse_scores, mae_scores, r2_scores = models_rating

    print(names, mse_scores, mae_scores, r2_scores, sep="\n\n")

    sns.set_style("darkgrid")
    plt.figure(figsize=(20,10))

    sns.barplot(x=r2_scores, y=names)
    plt.xlabel("r2_score")
    plt.ylabel("Названия моделей")
    plt.savefig(f"models_charts/r2_scores")
    
    sns.barplot(x=mse_scores, y=names)
    plt.xlabel("Mean-Squared-Error")
    plt.ylabel("Названия моделей")
    plt.savefig(f"models_charts/MSE")

    sns.barplot(x=mae_scores, y=names)
    plt.xlabel("Mean-Absolute-Error")
    plt.ylabel("Названия моделей")
    plt.savefig(f"models_charts/MAE")

