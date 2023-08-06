import keras
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.metrics import MeanSquaredError

def create_model (input_shape: int) -> keras.Model:
    model = Sequential()
    model.add(layer=Dense(units=100, activation="relu", input_shape=(input_shape,)))
    model.add(layer=Dropout(0.5))
    model.add(layer=Dense(units=100, activation="relu", kernel_regularizer=regularizers.l1(0.01)))
    model.add(layer=Dense(units=50, activation="relu", kernel_regularizer=regularizers.l2(0.01)))
    model.add(layer=Dense(units=1))

    model.compile(optimizer=RMSprop(learning_rate= 0.01), loss="mse", metrics=[MeanSquaredError()])

    return model
