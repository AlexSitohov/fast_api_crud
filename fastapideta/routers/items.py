from typing import Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapideta.database import get_db
from sqlalchemy.orm import Session
from fastapideta import models, oauth2
from fastapideta.schemas import Item, ItemResponse, ItemUpdate, User

router = APIRouter(tags=['items'])


@router.get('/items/', response_model=list[ItemResponse])
async def get_items(q: Union[int, None] = Query(default=None, description='category id filter'),
                    db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    if q is not None:
        items = db.query(models.Item).filter(models.Item.category_id == q).all()
    return items


@router.get('/items/{item_id}/', response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found!!!")
    return item


@router.post('/items/', response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, db: Session = Depends(get_db)):
    # new_item = models.Item(title=item.title, text=item.text, date_created=item.date_created,
    #                        category_id=item.category_id)
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.delete('/items/{item_id}/')
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_delete = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(item_delete)
    db.commit()
    return {'msg': 'success deleted'}


@router.put('/items/{item_id}/', response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    item_put = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_put:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found!!!')
    item_put.title = item.title
    item_put.text = item.text

    db.commit()
    db.refresh(item_put)
    return item_put
