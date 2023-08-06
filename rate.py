import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from preprocess import preprocess
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor, BaggingRegressor, AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import keras
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop, Adam
from keras.metrics import MeanSquaredError

## \brief Функция для создания собственной модели машинного обучения
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param[in] input_shape Определяет количество входных признаков для входного слоя. input_shape=len(X.columns)
## \return Скомпилированная модель Keras
def create_model (input_shape: int) -> keras.Model:
    model = Sequential()
    model.add(layer=Dense(units=100, activation="relu", input_shape=(input_shape,)))
    model.add(layer=Dropout(0.5))
    model.add(layer=Dense(units=100, activation="relu", kernel_regularizer=regularizers.l1(0.01)))
    model.add(layer=Dense(units=50, activation="relu", kernel_regularizer=regularizers.l2(0.01)))
    model.add(layer=Dense(units=1))

    model.compile(optimizer=Adam(learning_rate= 0.01), loss="mse", metrics=[MeanSquaredError()])

    return model

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

    model = create_model(input_shape=len(X.columns))
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

models_rating = rate_models(X,Y,verbose=False)
create_models_charts(models_rating)