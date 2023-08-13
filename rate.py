import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor, BaggingRegressor, AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from preprocess import preprocess
from create_model import create_model
## \brief Функция для создания собственной модели машинного обучения
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param[in] input_shape Определяет количество входных признаков для входного слоя. input_shape=len(X.columns)
## \return Скомпилированная модель Keras

## \brief Словарь с предобработанными данными, признаками и целевым переменными
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
data_preprocessed_dict = preprocess("data/houses-data_kaggle.csv")

## \brief Признаки данных
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
X = data_preprocessed_dict["X"]

## \brief Целевые переменные данных
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
Y = data_preprocessed_dict["Y"]

## \brief Функция-оценщик моделей
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param[in] X Признаки входных данных 
## \param[in] Y Целевые переменные входных данных 
## \param[in] verbose Аргумент определяет вывод на экран результаты обучения моделей. По умолчанию = True
## \return Кортеж tuple(), содержащий названия моделей и результаты их обучения ( mse, mae, r2_score )
def rate_models (X: pd.DataFrame, Y: pd.DataFrame, verbose=True) -> tuple:
    model = create_model(input_shape=len(X.columns))

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
            print(f"{name}:\nmean_squared_error: {mse}\nmean_absolute_error: {mae}\nr2_score: {r2}")

    model = create_model(input_shape=X.shape[1])
    model.fit(x_train, y_train, batch_size=64, epochs=30, verbose=0)
    y_pred = model.predict(x_test)
    
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    names.append("MyModelRegression")
    mse_scores.append(mse)
    mae_scores.append(mae)
    r2_scores.append(r2)

    if verbose:
        print(f"MyModelRegression:\nmean_squared_error: {mse}\nmean_absolute_error: {mae}\nr2_score: {r2}")
            
    return (names, mse_scores, mae_scores, r2_scores)
     
## \brief Функция построения графиков рейтинга моделей
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param[in] X Признаки входных данных 
## \param[in] Y Целевые переменные входных данных 
## \param[in] verbose Аргумент определяет вывод на экран результаты обучения моделей. По умолчанию = True
## \return None
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


def get_best_models (models_rating: tuple) -> dict:
    best_models = {
        "min_mse": list,
        "min_mae": list,
        "max_r2_score": list
    }
    names, mse_scores, mae_scores, r2_scores = models_rating
    
    min_mse, min_mae, max_r2_score = 10**10, 10**10, 0
    index_min_mse, index_min_mae, index_max_r2_score = 0, 0, 0


#models_rating = rate_models(X, Y, verbose=False)
models_rating = (['LinearRegression', 'HistGradientBoostingRegressor', 'ExtraTreesRegressor', 'BaggingRegressor', 'AdaBoostRegressor', 'RandomForestRegressor', 'GradientBoostingRegressor', 'DecisionTreeRegressor', 'MyModelRegression'], [2.6753618155175763e+32, 55224694775.27331, 102613580043.68875, 65799543072.58395, 84022389107.41452, 78872990158.12392, 52203744209.77829, 93220689035.20511, 44242259436.58469], [766385113772851.4, 133903.85964957363, 130826.03447553428, 125955.01790822748, 208457.5247483247, 128227.21714573719, 128100.39584306322, 157284.26429708343, 113579.19181830296], [-1.7983160514192346e+21, 0.6287924329596177, 0.31025535680504435, 0.557710759729195, 0.43522102268913276, 0.4698340859838226, 0.6490985607549817, 0.3733921877630646, 0.7026138115809493])

get_best_models(models_rating)