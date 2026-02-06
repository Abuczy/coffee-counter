from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from .database import Base


# Model SQLAlchemy (tabela w bazie)
class Coffee(Base):
    __tablename__ = "coffees"

    id = Column(Integer, primary_key=True, index=True)
    coffee_type = Column(String, default="espresso")
    size = Column(String, default="medium")  # small, medium, large
    created_at = Column(DateTime, default=datetime.now)


# Schematy Pydantic (walidacja danych)
class CoffeeCreate(BaseModel):
    coffee_type: Optional[str] = "espresso"
    size: Optional[str] = "medium"


class CoffeeResponse(BaseModel):
    id: int
    coffee_type: str
    size: str
    created_at: datetime

    class Config:
        from_attributes = True
