


from fastapi import APIRouter, Depends, HTTPException, Request
import joblib
from sqlalchemy.orm import Session
from app.db.dependencies import getdb
from app.schemas.employee_schema import employee_schema
from app.services.auth_service import decode_token, verify_user_in_db
import os
import sys
import pandas as pd
router= APIRouter(
    prefix="/predict",
    tags=["Prediction"] 
)
WORKDIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
model_path= os.path.join(WORKDIR, "ml","models", "saved_model", "model.pkl")

@router.post('/')
def predict(employee: employee_schema, request:Request, db:Session= Depends(getdb)):
    print('hello')
    token= request.cookies.get('token')
    if not token:
        raise HTTPException(status_code=401, detail="token not exist")
    payload= decode_token(token)
    if not verify_user_in_db(payload["username"], db):
        raise HTTPException(status_code=500, detail='user does not have access')

    employee_dict= employee.model_dump()
    employee_df= pd.DataFrame([employee_dict])
    model= joblib.load(model_path)
    prediction= model.predict(employee_df)

    print(prediction)
    return employee
    