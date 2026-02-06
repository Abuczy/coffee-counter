from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List

from .database import get_db, engine
from . import models

# Tworze tabele w bazie
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Coffee Counter ☕",
    description="Śledź ile kaw wypijasz dziennie!",
    version="1.0.0"
)


@app.get("/")
def root():
    """Strona główna"""
    return {"message": "Witaj w Coffee Counter! ☕", "docs": "/docs"}


@app.post("/coffee", response_model=models.CoffeeResponse)
def add_coffee(coffee: models.CoffeeCreate, db: Session = Depends(get_db)):
    """Dodaj kawę"""
    db_coffee = models.Coffee(
        coffee_type=coffee.coffee_type,
        size=coffee.size,
        created_at=datetime.now()
    )
    db.add(db_coffee)
    db.commit()
    db.refresh(db_coffee)
    return db_coffee


@app.get("/coffee", response_model=List[models.CoffeeResponse])
def get_all_coffees(db: Session = Depends(get_db)):
    """Pobierz wszystkie kawy"""
    return db.query(models.Coffee).order_by(models.Coffee.created_at.desc()).all()


@app.get("/coffee/today", response_model=List[models.CoffeeResponse])
def get_today_coffees(db: Session = Depends(get_db)):
    """Pobierz dzisiejsze kawy"""
    today = date.today()
    return db.query(models.Coffee).filter(
        func.date(models.Coffee.created_at) == today
    ).all()


@app.get("/coffee/stats")
def get_stats(db: Session = Depends(get_db)):
    """Statystyki kawowe"""
    today = date.today()

    total = db.query(models.Coffee).count()
    today_count = db.query(models.Coffee).filter(
        func.date(models.Coffee.created_at) == today
    ).count()

    # Najpopularniejszy typ kawy
    favorite = db.query(
        models.Coffee.coffee_type,
        func.count(models.Coffee.id).label('count')
    ).group_by(models.Coffee.coffee_type).order_by(
        func.count(models.Coffee.id).desc()
    ).first()

    return {
        "total_coffees": total,
        "today_coffees": today_count,
        "favorite_type": favorite[0] if favorite else None,
        "message": "Za dużo kawy!" if today_count > 5 else "Możesz się jeszcze napić ☕"
    }


@app.delete("/coffee/{coffee_id}")
def delete_coffee(coffee_id: int, db: Session = Depends(get_db)):
    """Usuń kawę (np. pomyłka)"""
    coffee = db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Nie znaleziono kawy")
    db.delete(coffee)
    db.commit()
    return {"message": "Kawa usunięta", "id": coffee_id}


@app.get("/health")
def health_check():
    """Health check dla Dockera"""
    return {"status": "healthy"}
