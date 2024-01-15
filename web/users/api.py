from uuid import UUID

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from database import SessionLocal, User
from models.user_models import UserCreate, UserRead, UserUpdate

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        email=user.email,
        password=bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode(),
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).one()
        return user
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id)
    if not db_user.first():
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_update.dict(exclude_unset=True)

    if "password" in user_data:
        hashed_password = bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt())
        user_data["password"] = hashed_password.decode()

    db_user.update(user_data)
    db.commit()
    return db_user.first()
