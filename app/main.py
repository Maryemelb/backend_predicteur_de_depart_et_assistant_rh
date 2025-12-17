from app.db.database import Base,engine
from fastapi import FastAPI
from sqlalchemy_utils import database_exists, create_database
from app.routes.register import router as register_router
from app.routes.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
app=FastAPI()
PORT = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

origins=[
    "http://localhost:3000", 
    "http://localhost:3001", 
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://backend:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(bind=engine)


app.include_router(register_router)
app.include_router(login_router)