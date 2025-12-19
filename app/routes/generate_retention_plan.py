

from fastapi import APIRouter, Depends
from pytest import Session

from app.db.dependencies import getdb
from app.models.employee import employee as Employee
from app.services.gemini_service import retention
router= APIRouter(
     prefix="/retention_generation",
    tags=["retention"]
)
@router.post('/{empid}')
def generateRetention(empid: int, db:Session= Depends(getdb)):
    employee= db.query(Employee).filter(Employee.id == empid).first()
    retention_plan= retention(employee.Age, employee.BusinessTravel, employee.Department, employee.Education, employee.EducationField, employee.EnvironmentSatisfaction, employee.Gender, employee.JobInvolvement, employee.JobLevel, employee.JobRole, employee.JobSatisfaction, employee.MaritalStatus, employee.MonthlyIncome, employee.OverTime, employee.PerformanceRating, employee.RelationshipSatisfaction, employee.StockOptionLevel, employee.TotalWorkingYears, employee.WorkLifeBalance, employee.YearsAtCompany, employee.YearsInCurrentRole, employee.YearsWithCurrManager, employee.Attrition)
    return retention_plan
