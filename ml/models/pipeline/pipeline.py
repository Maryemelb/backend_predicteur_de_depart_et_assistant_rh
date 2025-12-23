import pandas as pd
import sys
import os
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import accuracy_score, classification_report, f1_score, recall_score
import joblib

BASE_DIR= os.path.dirname(os.path.abspath(__file__))
data_path=os.path.join(BASE_DIR, '..', 'dataset', 'employees_dataset.csv')


def cleaning(data):
    data['Attrition']= data['Attrition'].map({'No':0, 'Yes':1})
    #I deleted 12 columns
    data= data.drop(columns=['EmployeeCount', 'Over18','DistanceFromHome','StandardHours','YearsSinceLastPromotion', 'TrainingTimesLastYear','PercentSalaryHike','NumCompaniesWorked','DailyRate','HourlyRate','MonthlyRate', 'EmployeeNumber'])
    return data

def split_data(prepared_data):
    X= prepared_data.drop(columns='Attrition', axis=1)
    y= prepared_data['Attrition']
    X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=0.30)
    return X_train, X_test, y_train, y_test


def pre_processing(data, smote, robust):
      data['Attrition']= data['Attrition'].map({'No':0, 'Yes':1})
      data= data.drop(columns=['EmployeeCount', 'Over18','DistanceFromHome','StandardHours','YearsSinceLastPromotion', 'TrainingTimesLastYear','PercentSalaryHike','NumCompaniesWorked','DailyRate','HourlyRate','MonthlyRate', 'EmployeeNumber'])
      X_train, X_test, y_train, y_test= split_data(data)
      X_cat= ['JobRole', 'BusinessTravel', 'Department', 'EducationField', 'Gender','JobLevel','MaritalStatus', 'OverTime','StockOptionLevel']
      X_num= ['MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsWithCurrManager']
      if(robust==1):
            preprocessor= ColumnTransformer(
            transformers= [
              ('num', RobustScaler(), X_num),
             ('cat', OneHotEncoder(handle_unknown='ignore'), X_cat),  
          ],
        remainder='passthrough'
          ) 
      else:   
          preprocessor= ColumnTransformer(
          transformers= [
             ('cat', OneHotEncoder(handle_unknown='ignore'), X_cat),  
          ],
        remainder='passthrough'
          )         
      if smote==1:
              pipeline_rf= Pipeline([
              ('preprocessor', preprocessor),
              ('smoting', SMOTE()),
              ('random', RandomForestClassifier())
        ])
              pipeline_lr= Pipeline([
              ('preprocessor', preprocessor),
              ('smoting', SMOTE()),
              ('logistic', LogisticRegression())
      ])
      else:
               pipeline_rf= Pipeline([
              ('preprocessor', preprocessor),
              ('random', RandomForestClassifier())
        ])
               pipeline_lr= Pipeline([
              ('preprocessor', preprocessor),
              ('logistic', LogisticRegression())
])
      param_grid_rf = {
         "random__n_estimators": [100, 300],
         "random__max_depth": [None, 30],
        }



      param_grid_lr = {
     'logistic__C': [0.1, 1, 10],         
    'logistic__solver': ['liblinear', 'saga'], 
    'logistic__class_weight': [None, 'balanced'] 
        }         
    
      return pipeline_rf,param_grid_rf,pipeline_lr, param_grid_lr, X_train, X_test, y_train, y_test
      

def gridsearch_metrics(pipline_param, gridparam ,  X_train, X_test, y_train, y_test):
    grid_search_cv=GridSearchCV(pipline_param, gridparam, cv=5,n_jobs=-1,verbose=2, scoring='f1')
    grid_search_cv.fit(X_train, y_train)
    y_predict= grid_search_cv.predict(X_test)
    y_pred_proba = grid_search_cv.predict_proba(X_test)[:, 1] 
    accuracy= accuracy_score(y_test, y_predict)
    recall= recall_score(y_test, y_predict)
    f1score= f1_score(y_test, y_predict)
    print(f'accuracy: {accuracy}')
    print(f'recall: {recall}')
    print(f'f1score: {f1score}')
    model_dir= 'ml/models/saved_model'
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(grid_search_cv.best_estimator_, os.path.join(model_dir, "model.pkl"))
    return y_pred_proba, y_predict

# data= pd.read_csv(data_path)
# pipeline_rf,param_grid_rf,pipeline_lr, param_grid_lr, X_train, X_test, y_train, y_test= pre_processing(data)

# print("Logistique regression: ")
# y_predict_proba_lr= gridsearch_metrics(pipeline_lr, param_grid_lr, X_train, X_test, y_train, y_test)
# print(y_predict_proba_lr)