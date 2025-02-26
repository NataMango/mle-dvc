# scripts/fit.py

# scripts/fit.py

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from category_encoders import CatBoostEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from catboost import CatBoostClassifier
import yaml
import os
import joblib


#params:
#index_col: 'customer_id'
#target_col: 'target'
#one_hot_drop: 'if_binary'
#auto_class_weights: 'Balanced'
#n_splits: 5
#metrics: ['f1', 'roc_auc']
#n_jobs: -1 
# params['index_col']

# обучение модели
def fit_model():
	# Прочитайте файл с гиперпараметрами params.yaml
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
      
    # загрузите результат предыдущего шага: initial_data.csv
    data = pd.read_csv('data/initial_data.csv')#.drop(columns=params['index_col'])
    
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
    ('cat', CatBoostEncoder(return_df=False), other_cat_features.columns.tolist()),
    ('num', StandardScaler(), num_features.columns.tolist())
    ],
    remainder='drop',
    verbose_feature_names_out=False
    )

    model = CatBoostClassifier(auto_class_weights=params['auto_class_weights']) #auto_class_weights='Balanced'

    pipeline = Pipeline(
    [
        ('preprocessor', preprocessor),
        ('model', model)
    ]
    )
    pipeline.fit(data, data['target']) #data, data['target']
    
    # сохраните обученную модель в models/fitted_model.pkl
    os.makedirs('models', exist_ok=True) # создание директории, если её ещё нет
    joblib.dump(pipeline, 'models/fitted_model.pkl')

if __name__ == '__main__':
	fit_model()
