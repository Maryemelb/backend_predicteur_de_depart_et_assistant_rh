
import pytest

from unittest.mock import Mock

from app.services.gemini_service import retention

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
def test_retention(mocker):
     fake_response= mocker.Mock()
     fake_response.text= "resumed text"

     fake_client= mocker.Mock()
     mocker.patch('app.services.gemini_service.genai.Client', return_value= fake_client)

     fake_client.models.generate_content.return_value = fake_response
  
     result= retention(employee.Age, employee.BusinessTravel, employee.Department, employee.Education, employee.EducationField, employee.EnvironmentSatisfaction, employee.Gender, employee.JobInvolvement, employee.JobLevel, employee.JobRole, employee.JobSatisfaction, employee.MaritalStatus, employee.MonthlyIncome, employee.OverTime, employee.PerformanceRating, employee.RelationshipSatisfaction, employee.StockOptionLevel, employee.TotalWorkingYears, employee.WorkLifeBalance, employee.YearsAtCompany, employee.YearsInCurrentRole, employee.YearsWithCurrManager, employee.Attrition)
     assert result == fake_response.text
     assert isinstance(result, str)