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

## \brief Функция расчета лучшей модели по трем метрикам
## \authors ivan-dev-lab-home
## \version 1.0.0
## \date 13.08.2023
## \param[in] models_rating Рейтинг моделей, полученный из функции rate_models 
## \details Программа ищет минимальную метрику из каждого массива ( mse_scores, mae_scores, r2_scores)
## \details Далее в массиве names происходит поиск имени модели по индексу минимальной ( в случае r2_scores - максимальной) метрики в массиве ( mse_scores, mae_scores, r2_scores)
## \code
# best_models["mse"] = [names[mse_scores.index(min(mse_scores))], min(mse_scores)]
# best_models["mae"] = [names[mae_scores.index(min(mae_scores))], min(mae_scores)]
# best_models["r2_score"] = [names[r2_scores.index(max(r2_scores))], max(r2_scores)]
## \endcode
## \brief Пример использования:
## \code
# models_rating = rate_models(X, Y, verbose=False)
# best_models = get_best_models(models_rating)
# for metric, result in best_models.items():
#     print(f"Метрика {metric} - лучший результат у {result[0]} = {result[1]}")
## \endcode
## \return None
def get_best_models (models_rating: tuple) -> dict:
    best_models = {
        "mse": list,
        "mae": list,
        "r2_score": list
    }
    names, mse_scores, mae_scores, r2_scores = models_rating
    
    best_models["mse"] = [names[mse_scores.index(min(mse_scores))], min(mse_scores)]
    best_models["mae"] = [names[mae_scores.index(min(mae_scores))], min(mae_scores)]
    best_models["r2_score"] = [names[r2_scores.index(max(r2_scores))], max(r2_scores)]

    return best_models