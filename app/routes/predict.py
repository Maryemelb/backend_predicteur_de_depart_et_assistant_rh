


from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.dependencies import getdb
from app.schemas.employee_schema import employee_schema
from app.services.auth_service import decode_token, verify_user_in_db
from app.models.employee import employee as EmpModel
from app.models.predictions_history import predictions_history as PridictionHistory
import os
import sys
import pandas as pd

from app.services.ml_service import chargeModel_prediction
router= APIRouter(
    prefix="/predict",
    tags=["Prediction"] 
)


@router.post('/')
async def predict(employee: employee_schema, request:Request,response:RedirectResponse, db:Session= Depends(getdb)):
    token= request.cookies.get('token')
    if not token:
        raise HTTPException(status_code=401, detail="token not exist")
    payload= decode_token(token)
    if not verify_user_in_db(payload["username"], db):
        raise HTTPException(status_code=500, detail='user does not have access')

    employee_dict= employee.model_dump()
    employee_df= pd.DataFrame([employee_dict])

    prediction, confident= chargeModel_prediction(employee_df)     
    #add emp to db
    emp_db= EmpModel(**employee_dict, Attrition=int(prediction))
    db.add(emp_db)
    db.commit()
    db.refresh(emp_db)
    emp_id= db.query(EmpModel).filter(EmpModel.id == emp_db.id).first()
    print(emp_id.id)
    # add to prediction hystory
    if(int(prediction) ==1):
            user_id_from_token= payload['id']
            new_churn_case= PridictionHistory(
                 userid = user_id_from_token,
                 employeeid= emp_id.id,
                 probability= float(confident)
            )
            db.add(new_churn_case)
            db.commit()
            db.refresh(new_churn_case)
    if float(confident) >= 0.5:
       
         response= RedirectResponse(url=f'/retention_generation/{emp_id.id}/{confident}', status_code=307)
         response.set_cookie(key='token',value=request.cookies.get('token'))
         
    return response
    