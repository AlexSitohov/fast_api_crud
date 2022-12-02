from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..hashing import bcrypt
from .. import models
from .. import schemas
from ..database import get_db

router = APIRouter(tags=['users'])


@router.post('/users/')
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user = models.User(name=user.name, password=bcrypt(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get('/users/')
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.delete('/users/{user_id}/')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {'msg': 'deleted'}
