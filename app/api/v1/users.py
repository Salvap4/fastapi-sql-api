from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.schemas.user import UserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/Users", tags=["users"])

# Dependency: create & close DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Unique email check
    exists = db.execute(
        select(models.User).where(models.User.email == payload.email)
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = models.User(full_name=payload.full_name, email=payload.email)
    db.add(user)
    db.commit()           # persist to DB
    db.refresh(user)    # reload from DB (now has id, created_at)
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)     # SQLAlchemy 2.0 way
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    result = db.execute(select(models.User).order_by(models.User.id.desc()))
    return result.scalars().all()

@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if payload.email and payload.email != user.email:
        exists = db.execute(
            select(models.User).where(models.User.email == payload.email)
        ).scalar_one_or_none()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = payload.email
    
    if payload.full_name:
        user.full_name = payload.full_name
        
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None
