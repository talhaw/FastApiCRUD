import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, User
from models.user_models import UserCreate, UserRead

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


# @router.post("/users/", response_model=UserRead)
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     pass  # Replace with actual code

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
