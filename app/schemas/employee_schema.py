
from pydantic import BaseModel
from typing import Literal


class employee_schema(BaseModel):
    Age: int

    Attrition: Literal["Yes", "No"]

    BusinessTravel: Literal[
        "Non-Travel",
        "Travel_Rarely",
        "Travel_Frequently"
    ]

    DailyRate: int

    Department: Literal[
        "Sales",
        "Research & Development",
        "Human Resources"
    ]

    DistanceFromHome: int
    Education: int

    EducationField: Literal[
        "Life Sciences",
        "Medical",
        "Marketing",
        "Technical Degree",
        "Human Resources",
        "Other"
    ]

    EmployeeCount: int
    EmployeeNumber: int
    EnvironmentSatisfaction: int

    Gender: Literal["Male", "Female"]

    HourlyRate: int
    JobInvolvement: int
    JobLevel: int

    JobRole: Literal[
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Sales Representative",
        "Research Director",
        "Human Resources"
    ]

    JobSatisfaction: int

    MaritalStatus: Literal[
        "Single",
        "Married",
        "Divorced"
    ]

    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int

    Over18: Literal["Y"]

    OverTime: Literal["Yes", "No"]

    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StandardHours: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int
