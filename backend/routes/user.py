from models.user import UserDetailsUpdate
from models.user import UserSetupPassword
from helpers.validators import validate_pesel
from helpers.generators import return_registration_code
from db_models.models import Teacher, Parent, Student, Principal, Worker, Admin, RegisterCode
from datetime import timedelta, datetime
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
            newUser.email = data.email
            newUser.address = data.address
            try:
                validate_pesel(data.PESEL)
                newUser.PESEL = data.PESEL
            except Exception as e:
                raise HTTPException(400, str(e))
            if isinstance(newUser, Student):
                if data.dateOfBirth is not None:
                    newUser.dateOfBirth = data.dateOfBirth
                else:
                    raise HTTPException(400, "No date of birth.")
            session.add(newUser)
            session.flush()
            newCode = RegisterCode(
                code=return_registration_code(),
                user_id=newUser.id,
            )
            session.add(newCode)
            session.flush()
            response = {"type": "Success", "message": "User registered successfully.", "registration_code": newCode.code}
            return JSONResponse(content=response)

@router.post("/activate", tags=["User", "Activate"])
def activate_user(data: UserSetupPassword) -> UserView:
    with get_session() as session:
        query = select(RegisterCode).where(RegisterCode.code == data.flogin_code)
        code = session.execute(query).scalar_one_or_none()
        if not code:
            raise HTTPException(404, "Invalid registration code.")
        if code.valid_for < datetime.now():
            raise HTTPException(400, "Registration code has expired.")
        query = select(User).where(User.id == code.user_id)
        user = session.execute(query).scalar_one_or_none()
        if not user:
            raise HTTPException(404, "User not found.")
        if data.password != data.confirm_password:
            raise HTTPException(400, "Passwords do not match.")
        user.hashed_password = get_password_hash(data.password)
        user.disabled = False
        session.delete(code)
        session.flush()
        return user


@router.delete("/{user_id}/deactivate", tags=["User", "Deactivate"])
def deactivate_user(user_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> UserView:
    if current_user.role in (UserRole.ADMIN, UserRole.PRINCIPAL):
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
    
@router.patch("/{user_id}/update", tags=["User", "Update"])
def update_user(user_id: int, data: UserDetailsUpdate, current_user: Annotated[User, Depends(get_current_active_user)]) -> UserView:
    with get_session() as session:
        query = select(User).where(User.id == user_id)
        user = session.execute(query).scalar_one_or_none()
        if not user:
            raise HTTPException(404, "User not found.")
        if current_user.role in (UserRole.ADMIN, UserRole.PRINCIPAL):
            if data.firstName is not None:
                user.firstName = data.firstName
            if data.lastName is not None:
                user.lastName = data.lastName
            if data.email is not None:
                user.email = data.email
            if data.phone is not None:
                user.phone = data.phone
            if data.PESEL is not None:
                user.PESEL = data.PESEL
            session.flush()
            return user
        else:
            raise HTTPException(401, "Invalid permissions for given action.")

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