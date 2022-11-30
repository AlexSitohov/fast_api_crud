from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import *

router = APIRouter()


@router.post('/categories/', tags=['categories'])
async def create_category(category: Category, db: Session = Depends(get_db)):
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get('/categories/', tags=['categories'])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@router.get('/categories/{category_id}/', tags=['categories'])
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return category


@router.delete('/categories/{category_id}/', tags=['categories'])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    db.delete(category)
    db.commit()
    return {'msg': 'deleted'}


@router.put('/categories/{category_id}/', tags=['categories'])
async def update_category(category_id: int, category: Category, db: Session = Depends(get_db)):
    category_update = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    category_update.name = category.name
    db.commit()
    db.refresh(category_update)
    return category_update
