import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from preprocess import preprocess
from rate import rate_models, create_models_charts, create_model

data_preprocessed_dict = preprocess("data/houses-data_raw.csv")

houses_data = data_preprocessed_dict["data_preprocessed"]
X = data_preprocessed_dict["X"]
Y = data_preprocessed_dict["Y"]

# Проведя сравнение, выяснилось, что средняя оценка всех моделей, участвовавших в рейтинге ( см. rate.py ) колеблется в диапазоне [0.45, 0.54]. Следовательно, проблема не в моделях, а в исходных даннных. 
# Проект будет временно приостановлен, пока не будут найдены новые данные, на которых будет лучше проводить обучение