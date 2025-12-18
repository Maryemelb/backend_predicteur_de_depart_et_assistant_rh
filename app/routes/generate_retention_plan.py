

from fastapi import APIRouter, Depends
from pytest import Session

from app.db.dependencies import getdb
from app.models.employee import employee as Employee

router= APIRouter(
     prefix="/retention_generation",
    tags=["retention"]
)
@router.post('/{empid}')
def generateRetention(empid: int, db:Session= Depends(getdb)):
    employe= db.query(Employee).filter(Employee.id == empid).first()
    return {'h': empid}