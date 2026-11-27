from sqlalchemy.orm import selectinload
from sqlalchemy import select
from models.studentclass import StudentClassCreate
from models.studentclass import StudentClassView
from db_models.models import StudentClass, Student, Parent
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from typing import List

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, Token, authenticate_user, create_access_token, get_current_active_user, get_password_hash
from database import get_session
from db_models.models import User, UserRole
from models.user import UserCreate, UserView

router = APIRouter(prefix="/studentclass")

@router.get("/get/all", tags=["StudentClass", "View", "All"])
def get_all_classes(current_user: User = Depends(get_current_active_user)) -> List[StudentClassView]:
    if current_user.role in (UserRole.ADMIN, UserRole.PRINCIPAL, UserRole.TEACHER):
        with get_session() as session:
            classes = session.execute(select(StudentClass).options(selectinload(StudentClass.students))).scalars().all()
            return classes
    else:
        with get_session() as session:
            if current_user.role == UserRole.STUDENT:
                classes = session.execute(select(StudentClass).options(selectinload(StudentClass.students)).where(StudentClass.students.any(Student.id == current_user.id))).scalars().all()
                return classes
            elif current_user.role == UserRole.PARENT:
                classes = session.execute(select(StudentClass).options(selectinload(StudentClass.students)).where(StudentClass.students.any(Student.parents.any(Parent.id == current_user.id)))).scalars().all()
                return classes
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view student classes.")

@router.get("/get/{class_id}", tags=["StudentClass", "View", "Single"])
def get_class(class_id: int, current_user: User = Depends(get_current_active_user)) -> StudentClassView:
    with get_session() as session:
        cls = session.execute(select(StudentClass).options(selectinload(StudentClass.students)).filter(StudentClass.id == class_id)).scalars().one_or_none()
        if not cls:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student class not found.")
        if current_user.role in (UserRole.ADMIN, UserRole.PRINCIPAL, UserRole.TEACHER):
            return cls
        elif current_user.role == UserRole.STUDENT:
            if any(student.id == current_user.id for student in cls.students):
                return cls
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this student class.")
        elif current_user.role == UserRole.PARENT:
            if any(parent.id == current_user.id for student in cls.students for parent in student.parents):
                return cls
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this student class.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this student class.")

@router.post("/create", tags=["StudentClass", "Create"])
def create_class(class_data: StudentClassCreate, current_user: User = Depends(get_current_active_user)) -> StudentClassView:
    if current_user.role in (UserRole.ADMIN, UserRole.PRINCIPAL):
        with get_session() as session:
            if class_data.teacher_id is not None:
                teacher = session.query(User).filter(User.id == class_data.teacher_id, User.role == UserRole.TEACHER).first()
                if not teacher:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found.")
            new_class = StudentClass(
                year=class_data.year,
                symbol=class_data.symbol,
                homeroom_teacher=teacher if class_data.teacher_id is not None else None,
                students=[]
            )
            session.add(new_class)
            session.commit()
            return new_class
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to create a student class.")