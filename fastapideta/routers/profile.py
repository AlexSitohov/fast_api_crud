from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import User, ChangePassword
from ..database import get_db
from .. import models, oauth2
from ..hashing import verify_password, bcrypt

router = APIRouter(tags=['profile'])


@router.put('/change/password/')
async def change_password(body: ChangePassword, db: Session = Depends(get_db),
                          current_user: User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.name == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid username')
    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    user.password = bcrypt(body.new_password)
    db.commit()
    db.refresh(user)
    return user
