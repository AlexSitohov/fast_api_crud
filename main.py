from fastapi import FastAPI, Depends, HTTPException, status, Query
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from schemas import *

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/items/')
async def get_items(q: int | None = Query(default=None, description='category id filter'),
                    db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    if q is not None:
        items = db.query(models.Item).filter(models.Item.category == q).all()
    return items


@app.get('/items/{item_id}/')
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found!!!")
    return item


@app.post('/items/', response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(title=item.title, text=item.text, date_created=item.date_created, category=item.category)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.delete('/items/{item_id}/')
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_delete = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(item_delete)
    db.commit()
    return {'msg': 'success deleted'}


@app.put('/items/{item_id}/', response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    item_put = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_put:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found!!!')
    # item_put = models.Item(title=item.title, text=item.text)
    item_put.title = item.title
    item_put.text = item.text

    db.commit()
    db.refresh(item_put)
    return item_put


@app.post('/categories/')
async def create_category(category: Category, db: Session = Depends(get_db)):
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get('/categories/')
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@app.get('/categories/{category_id}/')
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return category


@app.delete('/categories/{category_id}/')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    db.delete(category)
    db.commit()
    return {'msg': 'deleted'}


@app.put('/categories/{category_id}/')
async def update_category(category_id: int, category: Category, db: Session = Depends(get_db)):
    category_update = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    category_update.name = category.name
    db.commit()
    db.refresh(category_update)
    return category_update
