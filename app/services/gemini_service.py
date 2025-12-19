from google import genai
from google.genai import types
import os
from pydantic import BaseModel, Field

class Retention(BaseModel):
     recipe_name: str = Field(description="The retention plan.")
    

def retention(Age, BusinessTravel, Department, Education, EducationField,
EmployeeNumber, EnvironmentSatisfaction, Gender, JobInvolvement, JobLevel,
JobRole, JobSatisfaction, MaritalStatus, MonthlyIncome, OverTime,
PerformanceRating, RelationshipSatisfaction, StockOptionLevel, TotalWorkingYears,
WorkLifeBalance, YearsAtCompany, YearsInCurrentRole, YearsWithCurrManager):
   client = genai.Client(api_key=os.getenv('GEMINI_key'))
  

   prompt= f"""Agis comme un expert RH. 

   Voici les informations sur l’employé :
   - Age : {Age}
   - Département : {BusinessTravel}
   - Role : [JobRole]

   Contexte : ce salarié a un risque élevé de "churn_probability" de départ selon le modèle ML.  

    Tache : propose 3 actions concrètes et personnalisées pour le retenir dans l’entreprise, en tenant compte de son role, sa satisfaction, sa performance et son équilibre vie professionnelle/personnelle.  
     Rédige les actions de façon claire et opérationnelle pour un manager RH.

     """
   response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Retention.model_json_schema(),
    } 
    ) 
 
   retention = Retention.model_validate_json(response.text)
   return retention