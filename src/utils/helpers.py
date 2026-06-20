from fastapi import HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.utils.setting import settings
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db

# send token...
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        
        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
        
        return user
    except InvalidTokenError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")