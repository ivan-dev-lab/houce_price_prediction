import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import KFold, train_test_split
from keras import callbacks
from preprocess import preprocess
from rate import rate_models, create_models_charts
from create_model import create_model

def main ():
    ## \brief Словарь с обработанными данными, признаками и целевым переменными
    ## \authors ivan-dev-lab
    ## \version 1.0.0
    ## \date 05.08.2023
    data_preprocessed_dict = preprocess("data/houses-data_kaggle.csv")

    ## \brief Предобработанные данные
    ## \authors ivan-dev-lab
    ## \version 1.0.0
    ## \date 05.08.2023
    houses_data = data_preprocessed_dict["data"]

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

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    def train_model (x_train, x_test, y_train, y_test) -> dict:
        scores_dict = {
            "mse": float,
            "mae": float,
            "r2_score": float
        }

        model = create_model(x_train.shape[1])

        model.fit(x_train, y_train, batch_size=64, epochs=30, verbose=0)
        y_pred = model.predict(x_test)

        scores_dict["mse"] = mean_squared_error(y_test, y_pred)
        scores_dict["mae"] = mean_absolute_error(y_test, y_pred)
        scores_dict["r2_score"] = r2_score(y_test, y_pred)

        return scores_dict

    train_result = train_model (x_train, x_test, y_train, y_test)
    print(f"Итоговые результаты модели:\nmse = {train_result['mse']}\nmae = {train_result['mae']}\nr2_score = {train_result['r2_score']}")


if __name__ == "__main__":
    main()