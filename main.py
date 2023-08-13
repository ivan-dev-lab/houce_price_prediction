import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import KFold, train_test_split
from keras import Model
from preprocess import preprocess
from rate import rate_models, create_models_charts
from create_model import create_model

## \brief Главная функция для запуска кода
## \authors ivan-dev-lab
## \version 1.0.0
## \date 06.08.2023
## \param None
## \return None
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

    # предполагается, что во время использования этой функции как конечного продукта - пользователь будет выяснять по графикам - какая модель лучше, исходя из этого останавливая свой выбор на данной модели

    # models_rating = rate_models(X,Y,verbose=False)
    # create_models_charts(models_rating)

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    ## \brief Функция для тренировки модели
    ## \authors ivan-dev-lab
    ## \version 1.0.0
    ## \date 06.08.2023
    ## \param[out] model Параметр принимает созданную и скомпилированную модель, необходимую для дальнейшего обучения
    ## \param[in] x_train Одна из частей данных для тренировки модели. Содержит в себе 80% признаков из данных
    ## \param[in] x_test Одна из частей данных для тренировки модели. Содержит в себе 20% признаков из данных
    ## \param[in] y_train Одна из частей данных для тренировки модели. Содержит в себе 80% целевых переменных из данных
    ## \param[in] y_test Одна из частей данных для тренировки модели. Содержит в себе 20% целевых переменных из данных
    ## \return Словарь dict с такими метриками модели, как mse, mae, r2_score    
    def train_model (model: Model, x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame) -> dict:
        scores_dict = {
            "mse": float,
            "mae": float,
            "r2_score": float
        }

        model.fit(x_train, y_train, batch_size=64, epochs=30, verbose=0)
        y_pred = model.predict(x_test)

        scores_dict["mse"] = mean_squared_error(y_test, y_pred)
        scores_dict["mae"] = mean_absolute_error(y_test, y_pred)
        scores_dict["r2_score"] = r2_score(y_test, y_pred)

        return scores_dict

    model = create_model(x_train.shape[1])
    # print(model.get_config())

    train_result = train_model (model, x_train, x_test, y_train, y_test)

    print(f"Итоговые результаты модели:\nmse = {train_result['mse']}\nmae = {train_result['mae']}\nr2_score = {train_result['r2_score']}")

if __name__ == "__main__":
    main()