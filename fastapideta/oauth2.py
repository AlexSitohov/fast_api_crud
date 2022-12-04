from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapideta.JWT import verify_token

WRITE = {"all": "write_access"}  # this is used in user access verification method
READ = {"all": "read_access"}  # this is used in user access verification method

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT"
                                     )


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(data, credentials_exception)
