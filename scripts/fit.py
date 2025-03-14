# scripts/fit.py

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
#from category_encoders import CatBoostEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
#from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
import yaml
import os
import joblib

# обучение модели
def fit_model():
	# Прочитайте файл с гиперпараметрами params.yaml
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
      
    # загрузите результат предыдущего шага: initial_data.csv
    data = pd.read_csv('data/initial_data.csv') #02:38
    
    # реализуйте основную логику шага с использованием гиперпараметров
    # обучение модели
    cat_features = data.select_dtypes(include='object')
    potential_binary_features = cat_features.nunique() == 2

    binary_cat_features = cat_features[potential_binary_features[potential_binary_features].index]
    other_cat_features = cat_features[potential_binary_features[~potential_binary_features].index]
    num_features = data.select_dtypes(['float'])

    preprocessor = ColumnTransformer(
    [
    ('binary', OneHotEncoder(drop=params['one_hot_drop']), binary_cat_features.columns.tolist()),
    ('cat', OneHotEncoder(drop=params['one_hot_drop']), other_cat_features.columns.tolist()),
    ('num', StandardScaler(), num_features.columns.tolist())
    ],
    remainder='drop',
    verbose_feature_names_out=False
    )


    #model = CatBoostClassifier(auto_class_weights=params['auto_class_weights']) #auto_class_weights='Balanced'
    model = LogisticRegression(C=params['C'], penalty=params['penalty'])
    #print(model)
    pipeline = Pipeline(
    [
        ('preprocessor', preprocessor),
        ('model', model)
    ]
    )
    pipeline.fit(data, data['target']) 
    
    # сохраните обученную модель в models/fitted_model.pkl
    os.makedirs('models', exist_ok=True) # создание директории, если её ещё нет
    joblib.dump(pipeline, 'models/fitted_model.pkl')

if __name__ == '__main__':
	fit_model()

