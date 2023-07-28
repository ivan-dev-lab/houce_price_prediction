import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

def plot_scaler_data (scaler_score: dict, data_type: str, scaler_name: str, X: pd.DataFrame, fchart: str="charts/"):
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
    
    plt.figure(figsize=(10, 6))

    for i, data_row in enumerate(chart_data_full):
        plt.barh(X.columns, data_row, label=f"{data_type.lower().split('_')[i]}", alpha=0.5)


    plt.xlabel("Признаки")
    plt.ylabel("Значения")
    plt.title(f"{data_type} - {scaler_name}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def create_scaler_charts (score_scalers: dict, X: pd.DataFrame):
    for scaler_name, scaler_score_data in score_scalers.items():
        for scaler_score in scaler_score_data:
            if "MIN_MAX" in scaler_score:
                plot_scaler_data(scaler_score, "MIN_MAX", scaler_name, X)
            else:
                plot_scaler_data(scaler_score, "MEAN_STD", scaler_name, X)

