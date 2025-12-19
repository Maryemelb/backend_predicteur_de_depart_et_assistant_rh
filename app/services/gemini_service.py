from typing import List
from google import genai
from google.genai import types
import os
from pydantic import BaseModel, Field

class Retention(BaseModel):
     retention_plan: List[str]
    

def retention(Age, BusinessTravel, Department, Education, EducationField,
EmployeeNumber, EnvironmentSatisfaction, Gender, JobInvolvement, JobLevel,
JobRole, JobSatisfaction, MaritalStatus, MonthlyIncome, OverTime,
PerformanceRating, RelationshipSatisfaction, StockOptionLevel, TotalWorkingYears,
WorkLifeBalance, YearsAtCompany, YearsInCurrentRole, YearsWithCurrManager):
   client = genai.Client(api_key=os.getenv('GEMINI_key'))
  

   prompt= f"""Agis comme un expert RH. 

   Voici les informations sur l’employé :
      Âge : {Age}

      Voyages professionnels : {BusinessTravel}

      Département : {Department}

      Niveau d’éducation : {Education}

      Domaine d’éducation : {EducationField}

      Numéro d’employé : {EmployeeNumber}

      Satisfaction de l’environnement : {EnvironmentSatisfaction}

      Genre : {Gender}

      Implication au travail : {JobInvolvement}

      Niveau de poste : {JobLevel}

      Rôle du poste : {JobRole}

      Satisfaction au travail : {JobSatisfaction}

      Statut marital : {MaritalStatus}

      Revenu mensuel : {MonthlyIncome}

      Heures supplémentaires : {OverTime}

      Évaluation de la performance : {PerformanceRating}

      Satisfaction relationnelle : {RelationshipSatisfaction}

      Niveau d’options d’actions : {StockOptionLevel}

      Total des années d’expérience : {TotalWorkingYears}

      Équilibre vie professionnelle / personnelle : {WorkLifeBalance}

      Ancienneté dans l’entreprise : {YearsAtCompany}

      Ancienneté dans le poste actuel : {YearsInCurrentRole}

      Ancienneté avec le manager actuel : {YearsWithCurrManager}

   Contexte : ce salarié a un risque élevé de "churn_probability" de départ selon le modèle ML.  

    Tache : 
    -propose 4 actions concrètes et personnalisées pour le retenir dans l’entreprise, en tenant compte de son role, sa satisfaction, sa performance et son équilibre vie professionnelle/personnelle.  
     Rédige les actions de façon claire et opérationnelle pour un manager RH.
    - "retention_plan" doit être une LISTE (array) de 4 chaînes de caractères
    EXEMPLE :
  
          {{
          "retention_plan": [
            "Action 1",
            "Action 2",
            "Action 3",
            "Action 4"
          ]
        }}

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