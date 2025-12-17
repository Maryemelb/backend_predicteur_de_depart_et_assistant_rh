import pandas as pd
import sys
import os
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import accuracy_score, f1_score, recall_score
import joblib
BASE_DIR= os.path.dirname(os.path.abspath(__file__))
data_path=os.path.join(BASE_DIR, '..', 'dataset', 'employees_dataset.csv')

data= pd.read_csv(data_path)

def cleaning(data):
    data['Attrition']= data['Attrition'].map({'No':0, 'Yes':1})
    data= data.drop(columns=['EmployeeCount', 'Over18','StandardHours','HourlyRate','MonthlyRate', 'EmployeeNumber'])
    # categorial_columns= ['JobRole', 'BusinessTravel', 'Department', 'Education', 'EducationField', 'EnvironmentSatisfaction', 'Gender', 'JobInvolvement','JobLevel', 'JobSatisfaction','MaritalStatus', 'RelationshipSatisfaction' ,'PerformanceRating', 'OverTime','StockOptionLevel', 'WorkLifeBalance']
    # encoder= OneHotEncoder(sparse_output=False)
    # for col in categorial_columns:
    #     transformed_data= encoder.fit_transform(data[[col]])
    #     transformed_df= pd.DataFrame(
    #         transformed_data,
    #         columns= encoder.get_feature_names_out([col]),
    #         index= data.index
    #     )
    #     data=pd.concat([data.drop(columns=[col]), transformed_df], axis=1)
    return data

def split_data(prepared_data):
    X= prepared_data.drop(columns='Attrition', axis=1)
    y= prepared_data['Attrition']
    X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=0.30)
    return X_train, X_test, y_train, y_test

def training(X_train, X_test, y_train, y_test, model):
    if model==  RandomForestClassifier:
              rf= model()
    else :
              rf= model()


    rf.fit(X_train, y_train)
    y_predict= rf.predict(X_test)
    accuracy= accuracy_score(y_test, y_predict)
    recall= recall_score(y_test, y_predict)
    f1score= f1_score(y_test, y_predict)
    print(f'accuracy: {accuracy}')
    print(f'recall: {recall}')
    print(f'f1score: {f1score}')
    return f1score





# prepared_data= prepare_data(data)
# X_train, X_test, y_train, y_test= split_data(prepared_data)
# normalized_data= normalisation(prepared_data)
# print(normalized_data)
# training(X_train, X_test, y_train, y_test, LogisticRegression)
# training(X_train, X_test, y_train, y_test, RandomForestClassifier)

prepared_data= cleaning(data)
X_train, X_test, y_train, y_test= split_data(prepared_data)
X_cat= ['JobRole', 'BusinessTravel', 'Department', 'Education', 'EducationField', 'EnvironmentSatisfaction', 'Gender', 'JobInvolvement','JobLevel', 'JobSatisfaction','MaritalStatus', 'RelationshipSatisfaction' ,'PerformanceRating', 'OverTime','StockOptionLevel', 'WorkLifeBalance']
X_num= ['DistanceFromHome', 'MonthlyIncome', 'DailyRate','NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear','YearsAtCompany', 'YearsInCurrentRole','YearsSinceLastPromotion', 'YearsWithCurrManager']
preprocessor= ColumnTransformer(
   transformers= [
      ('num', RobustScaler(), X_num),
      ('cat', OneHotEncoder(), X_cat)
   ]
)
pipeline_rf= Pipeline([
   ('preprocessor', preprocessor),
   ('random', RandomForestClassifier())
])

param_grid_rf = {
    "random__n_estimators": [100, 300],
    "random__max_depth": [None, 30],
}

pipeline_lr= Pipeline([
   ('preprocessor', preprocessor),
   ('random', RandomForestClassifier())
])

param_grid_lr = {
    "random__n_estimators": [100, 300],
    "random__max_depth": [None, 30],
}

def gridsearch_metrics(pipline_param, gridparam ):
    grid_search_cv=GridSearchCV(pipline_param, gridparam, cv=5,n_jobs=-1,verbose=2, scoring='f1')
    grid_search_cv.fit(X_train, y_train)
    y_predict= grid_search_cv.predict(X_test)

    accuracy= accuracy_score(y_test, y_predict)
    recall= recall_score(y_test, y_predict)
    f1score= f1_score(y_test, y_predict)
    print(f'accuracy: {accuracy}')
    print(f'recall: {recall}')
    print(f'f1score: {f1score}')
    if pipline_param == pipeline_rf:
          model_dir= 'saved_model'
          os.makedirs(model_dir, exist_ok=True)
          joblib.dump(grid_search_cv.best_estimator_, os.path.join(model_dir, "random_forest_model.pkl"))
    return  f1score
print("Random forest: ")
gridsearch_metrics(pipeline_rf, param_grid_rf)

print("Logistique regression: ")
gridsearch_metrics(pipeline_lr, param_grid_lr)