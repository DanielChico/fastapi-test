from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import user_model
from ..schemas import user_schemas
from ..security import security


def get_user(db: Session, user_id: int) -> user_model.User:
    return db.get(user_model.User, user_id)


def get_user_by_username(db: Session, username: str) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def get_users_list(db: Session) -> list[user_model.User]:
    return db.query(user_model.User).all()


def create_user(db: Session, user: user_schemas.UserCreate) -> user_model.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = user_model.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db.delete(get_user(db=db, user_id=user_id))
    db.commit()



