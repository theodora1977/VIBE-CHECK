from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
import os
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
        
        # sign in the user by creating an account if they don't exist
@app.post("/signup/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.post("/login/", tags=["Users"])
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    # In a real app, use password hashing (e.g., bcrypt)
    if not db_user or db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    return {"message": "Login successful", "user_id": db_user.id}

@app.get("/login-ui", tags=["UI"])
def get_login_ui():
    # Serves the index.html file located in the parent directory
    return FileResponse(os.path.join(os.path.dirname(__file__), "../index.html"))

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.post("/businesses/", response_model=schemas.Business, tags=["Businesses"])
def create_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    return crud.create_business(db, business)

@app.get("/businesses/", response_model=list[schemas.Business], tags=["Businesses"])
def get_businesses(db: Session = Depends(get_db)):
    return crud.get_businesses(db)

@app.post("/reviews/", response_model=schemas.Review, tags=["Reviews"])
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)
