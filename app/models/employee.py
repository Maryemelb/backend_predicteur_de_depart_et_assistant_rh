
from sqlalchemy import Boolean, Column, Enum, Integer
from app.db.database import Base
class employee(Base):
   __tablename__= "employee"
   id=Column(Integer, primary_key=True)
   Age= Column(Integer, nullable=True)
   BusinessTravel=Column(Enum(
       "Non-Travel",
        "Travel_Rarely",
        "Travel_Frequently",
        name="business_travel_enum"
   ), nullable=True)

   Department= Column(Enum(
       "Sales",
        "Research & Development",
        "Human Resources",
        name="departement_enum"
   ), nullable= True)

   Education= Column(Integer, nullable=True)
   EducationField = Column(
        Enum(
            "Life Sciences",
            "Medical",
            "Marketing",
            "Technical Degree",
            "Human Resources",
            "Other",
            name="education_field_enum"
        ),
        nullable=True
    )

   EnvironmentSatisfaction = Column(Integer, nullable=True)

   Gender = Column(
        Enum("Male", "Female", name="gender_enum"),
        nullable=True
    )

   JobInvolvement = Column(Integer, nullable=True)
   JobLevel = Column(Integer, nullable=True)

   JobRole = Column(
        Enum(
            "Sales Executive",
            "Research Scientist",
            "Laboratory Technician",
            "Manufacturing Director",
            "Healthcare Representative",
            "Manager",
            "Sales Representative",
            "Research Director",
            "Human Resources",
            name="job_role_enum"
        ),
        nullable=True
    )

   JobSatisfaction = Column(Integer, nullable=True)

   MaritalStatus = Column(
        Enum(
            "Single",
            "Married",
            "Divorced",
            name="marital_status_enum"
        ),
        nullable=True
    )

   MonthlyIncome = Column(Integer, nullable=True)

   OverTime = Column(
        Enum("Yes", "No", name="overtime_enum"),
        nullable=True
    )

   PerformanceRating = Column(Integer, nullable=True)
   RelationshipSatisfaction = Column(Integer, nullable=True)
   StockOptionLevel = Column(Integer, nullable=True)
   TotalWorkingYears = Column(Integer, nullable=True)
   WorkLifeBalance = Column(Integer, nullable=True)

   YearsAtCompany = Column(Integer, nullable=True)

   YearsInCurrentRole = Column(Integer, nullable=True)

   YearsWithCurrManager = Column(Integer, nullable=True)

   Attrition = Column(Integer, nullable=True)