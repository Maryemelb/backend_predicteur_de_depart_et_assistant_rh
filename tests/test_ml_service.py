import pytest
import pandas as pd
from app.services.ml_service import chargeModel_prediction
@pytest.fixture
def employee():
    return {
  "Age": 15,
  "BusinessTravel": "Non-Travel",
  "Department": "Sales",
  "Education": 0,
  "EducationField": "Life Sciences",
  "EmployeeNumber": 0,
  "EnvironmentSatisfaction": 0,
  "Gender": "Male",
  "JobInvolvement": 0,
  "JobLevel": 0,
  "JobRole": "Sales Executive",
  "JobSatisfaction": 0,
  "MaritalStatus": "Single",
  "MonthlyIncome": 0,
  "OverTime": "Yes",
  "PerformanceRating": 0,
  "RelationshipSatisfaction": 0,
  "StockOptionLevel": 0,
  "TotalWorkingYears": 0,
  "WorkLifeBalance": 0,
  "YearsAtCompany": 0,
  "YearsInCurrentRole": 0,
  "YearsWithCurrManager": 0
}
def test_ml_service(employee):
    df = pd.DataFrame([employee])
    prediction, confident= chargeModel_prediction(df)
    assert prediction is not None
    assert confident is not None
    assert  int(prediction) ==1 or int(prediction)== 0
    assert  float(confident)>= 0 or float(confident) <= 0



