from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.users.dtos import UserSchema, UserResponseSchema, LoginSchema
from src.users import controller


user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model= UserResponseSchema ,status_code=status.HTTP_201_CREATED)
async def register(body: UserSchema, db: Session=Depends(get_db)):
    # username validation
    # Email validation
    return await controller.register(body, db)



@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session=Depends(get_db)):
    return controller.login_user(body, db)



@user_router.get("/is_auth",response_model= UserResponseSchema ,status_code=status.HTTP_200_OK)
def is_auth(request: Request,  db: Session=Depends(get_db)):
    return controller.is_authenticated(request, db)