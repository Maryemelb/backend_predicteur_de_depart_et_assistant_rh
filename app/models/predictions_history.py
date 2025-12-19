from app.db.database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from datetime import datetime

class predictions_history(Base):
    __tablename__= "predictions_history"
    id= Column(Integer,primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'))
    employeeid  = Column(Integer, ForeignKey('employee.id'))
    probability= Column(Float)
    timestamp = Column(DateTime, default= datetime.now )

