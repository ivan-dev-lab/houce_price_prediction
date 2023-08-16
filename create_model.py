import keras
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.metrics import MeanSquaredError

## \brief Функция для создания модели
## \authors ivan-dev-lab
## \version 1.0.0
## \date 06.08.2023
## \param[in] input_shape Размерность входных данных. Необходима для входного слоя модели
## \details Ниже представлен исходный код архитектуры модели
## \code
# model = Sequential()
# model.add(layer=Dense(units=100, activation="relu", input_shape=(input_shape,)))
# model.add(layer=Dropout(0.5))
# model.add(layer=Dense(units=100, activation="relu", kernel_regularizer=regularizers.l1(0.01)))
# model.add(layer=Dense(units=50, activation="relu", kernel_regularizer=regularizers.l2(0.01)))
# model.add(layer=Dense(units=1))
## \endcode
## \details Модель скомпилирована с использованием таких функций, как:
## <ol>
## <li>Функция-оптимизатор: <b>RMSprop</b> с фактором обучения: <b>0.01</b></li>
## <li>Функция потерь: <b>Mean-Squared-Error</b></li>
## <li>Метрики: <b>[ MeanSquaredError() ]</b></li>
## </ol>
## \details Ниже представлен исходный код компиляции модели
## \code
# model.compile(optimizer=RMSprop(learning_rate= 0.01), loss="mse", metrics=[MeanSquaredError()])
## \endcode
## \return keras.Model - скомпилированная, но не обученная модель
def create_model (input_shape: int) -> keras.Model:
    model = Sequential()
    model.add(layer=Dense(units=100, activation="relu", input_shape=(input_shape,)))
    model.add(layer=Dropout(0.5))
    model.add(layer=Dense(units=100, activation="relu", kernel_regularizer=regularizers.l1(0.01)))
    model.add(layer=Dense(units=50, activation="relu", kernel_regularizer=regularizers.l2(0.01)))
    model.add(layer=Dense(units=1))

    model.compile(optimizer=RMSprop(learning_rate= 0.01), loss="mse", metrics=[MeanSquaredError()])

    return model
