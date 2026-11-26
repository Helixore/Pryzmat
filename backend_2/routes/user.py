from backend_2.helpers.validators import validate_pesel
from backend_2.db_models.models import Teacher, Parent, Student, Principal, Worker, Admin
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, Token, authenticate_user, create_access_token, get_current_active_user, get_password_hash
from database import get_session
from db_models.models import User, UserRole
from models.user import UserCreate, UserView, UserAssignRole

router = APIRouter(prefix="/users")

@router.get("/self", tags=["User"])
def show_self(current_user: Annotated[User, Depends(get_current_active_user)]) -> UserView:
    return current_user

@router.post("/create", tags=["User", "Create"])
def register_user(data: UserCreate):
    class_dict = {
        UserRole.ADMIN: Admin,
        UserRole.PRINCIPAL: Principal,
        UserRole.TEACHER: Teacher,
        UserRole.WORKER: Worker,
        UserRole.PARENT: Parent,
        UserRole.STUDENT: Student
    }
    with get_session() as session:
        pq = select(User).where(User.username == data.username)
        result = session.execute(pq).scalar_one_or_none()
        if not result:
            newUser = class_dict.get(data.role)()
            newUser.username = data.username
            #newUser.hashed_password = get_password_hash(data.password)
            newUser.role = data.role
            newUser.firstName = data.firstName
            newUser.lastName = data.lastName
            newUser.PESEL = data.PESEL
            newUser.address = data.address
            if not validate_pesel(data.email):
                raise HTTPException(400, "Invalid PESEL.")
            newUser.email = data.email
            if isinstance(newUser, Student):
                if data.dateOfBirth is not None:
                    newUser.dateOfBirth = data.dateOfBirth
                else:
                    raise HTTPException(400, "No date of birth.")
            session.add(newUser)
            session.flush()
            response = {"type": "Success", "message": "User registered successfully."}
            return JSONResponse(content=response)

@router.delete("/{user_id}/deactivate")
def deactivate_user(user_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> UserView:
    if current_user in (UserRole.ADMIN, UserRole.PRINCIPAL):
        with get_session() as session:
            query = select(User).where(User.id == user_id)
            user = session.execute(query).scalar_one_or_none()
            if not user:
                raise HTTPException(404, "User not found.")
            user.disabled = True
            session.flush()
            return user
    else:
        raise HTTPException(401, "Invalid permissions for given action.")
    
@router.patch("/{user_id}/update")
def update_user(user_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> UserView:
    pass

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