from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auto Estimator Backend")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Auto Estimator Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router)
