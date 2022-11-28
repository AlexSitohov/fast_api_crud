from fastapi import FastAPI, Depends, HTTPException
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
async def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items


@app.get('/items/{item_id}/')
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found!!!")
    return item


@app.post('/items/', response_model=ItemResponse)
async def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(title=item.title, text=item.text, date_created=item.date_created)
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
    # item_put = models.Item(title=item.title, text=item.text)
    item_put.title = item.title
    item_put.text = item.text

    db.commit()
    db.refresh(item_put)
    return item_put
