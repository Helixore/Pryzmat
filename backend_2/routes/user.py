from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, Token, authenticate_user, create_access_token, get_current_active_user, get_password_hash
from database import get_session
from db_models.models import User, UserRole
from models.user import UserCreate, UserView

router = APIRouter(prefix="/users")

@router.get("/self", tags=["User"])
def show_self(current_user: Annotated[User, Depends(get_current_active_user)]) -> UserView:
    return current_user

@router.post("/register", tags=["User", "Register"])
def register_user(data: UserCreate):
    with get_session() as session:
        pq = select(User).where(User.username == data.username)
        result = session.execute(pq).scalar_one_or_none()
        if not result:
            if data.password == data.confirm_password:
                newUser: User = User()
                newUser.username = data.username
                newUser.hashed_password = get_password_hash(data.password)
                newUser.role = UserRole.UNASSIGNED
                session.add(newUser)
                session.flush()
                response = {"type": "Success", "message": "User registered successfully."}
                return JSONResponse(content=response)

@router.post("/login", tags=["User", "Login"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    with get_session() as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")