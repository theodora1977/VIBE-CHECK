from sqlalchemy.orm import Session
from . import models, schemas
from .vibe_engine import analyze_review
from sqlalchemy import func

def create_business(db: Session, business: schemas.BusinessCreate):
    db_business = models.Business(
        name=business.name,
        category=business.category,
        location=business.location,
        vibe_score=0.0
    )
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

def get_businesses(db: Session):
    return db.query(models.Business).all()

def create_review(db: Session, review: schemas.ReviewCreate):
    analysis = analyze_review(review.content)

    db_review = models.Review(
        user_id=review.user_id,
        business_id=review.business_id,
        content=review.content,
        vibe_score=analysis["vibe_score"],
        sentiment=analysis["sentiment"],
        keywords=", ".join(analysis["keywords"])
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # Recalculate business vibe score
    business = db.query(models.Business).filter(models.Business.id == review.business_id).first()
    if business:
        # Let the database calculate the new average score efficiently
        new_vibe_score = db.query(func.avg(models.Review.vibe_score)).filter(models.Review.business_id == review.business_id).scalar() or 0.0
        business.vibe_score = new_vibe_score
        db.commit()

    return db_review
