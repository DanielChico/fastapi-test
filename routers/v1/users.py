from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal, engine
from core.models import user_model
from core.schemas import user_schemas
from core.services import user_service
from core.security import security

router = APIRouter(
    prefix="/users",
)

user_model.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login")
async def log_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db=db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username doesn't exist")
    if not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Wrong password")


@router.post("/create")
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_service.create_user(db=db, user=user)


@router.get("/list")
async def read_users(db: Session = Depends(get_db)):
    users = user_service.get_users_list(db=db)
    return users


@router.get("/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/name/{username}")
async def read_user(username: str, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db=db, user_id=user_id)
