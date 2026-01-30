from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    location = Column(String)
    vibe_score = Column(Float, default=0.0)

    reviews = relationship("Review", back_populates="business")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    content = Column(Text)
    vibe_score = Column(Float)
    sentiment = Column(String)
    keywords = Column(String)

    business = relationship("Business", back_populates="reviews")