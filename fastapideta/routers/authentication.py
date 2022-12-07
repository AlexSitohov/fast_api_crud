from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..JWT import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from ..schemas import Login, User, ChangePassword
from ..database import get_db
from .. import models
from ..hashing import verify_password, bcrypt

router = APIRouter(tags=['authentication'])


@router.post('/login')
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid username')
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}
    )
    return {"access_token": access_token, "token_type": "bearer"}
