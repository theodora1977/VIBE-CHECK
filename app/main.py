from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VibeCheck API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/businesses/", response_model=schemas.Business, tags=["Businesses"])
def create_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    return crud.create_business(db, business)

@app.get("/businesses/", response_model=list[schemas.Business], tags=["Businesses"])
def get_businesses(db: Session = Depends(get_db)):
    return crud.get_businesses(db)

@app.post("/reviews/", response_model=schemas.Review, tags=["Reviews"])
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)
