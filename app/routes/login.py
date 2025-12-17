


from fastapi import APIRouter, Depends, HTTPException, Response
from app.models.users import users
from app.schemas.user_schema import user_schema
from app.db.dependencies import getdb
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.services.auth_service import create_token, decrypt_password
load_dotenv()
router=APIRouter(
    prefix='/Auth',
    tags=['Auth']
)




context= CryptContext(schemes=["argon2"], deprecated="auto")

def decrypt_password(inserted_pasword: str, hashed_password: str):
    return context.verify(inserted_pasword, hashed_password)

@router.post('/login')
def login(user: user_schema, response:Response, db:Session= Depends(getdb)):
          user_db= db.query(users).filter(users.username == user.username).first()  
          print('test')
          user_db= db.query(users).filter(users.username == user.username).first()
          print('test')
          if not user_db:
             raise HTTPException(status_code=400, detail='user not exist')
          if not decrypt_password(user.password, user_db.passwordhash):
              raise HTTPException(status_code=401, detail='wrong password')
          token = create_token(user.username)
          response.set_cookie(
               key='token',
               value= token,
               httponly=True,
               secure=True,     
               samesite="None",
               path="/" 
          )
          return {'message': 'login succesfully!'}