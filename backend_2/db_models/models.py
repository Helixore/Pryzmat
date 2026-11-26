
from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SQLAlchemyEnum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


# ============================================================
# ENUMS
# ============================================================

class ConductEntryType(str, Enum):
    POSITIVE = "POS"
    NEGATIVE = "NEG"
    NEUTRAL = "NEU"


class QuizType(str, Enum):
    TEST = "Sprawdzian"
    QUIZ = "Kartkówka"


# ============================================================
# USER
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(60))
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(128), nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean(), default=True, server_default="True")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "user",
    }
# ============================================================
# STUDENT CLASS
# ============================================================

class StudentClass(Base):
    __tablename__ = "student_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    symbol: Mapped[str] = mapped_column(String(10))

    homeroom_teacher: Mapped["Teacher | None"] = relationship(
        back_populates="form_tutor",
        uselist=False,
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="student_class"
    )

    subjects: Mapped[list["Subject"]] = relationship(
        back_populates="student_class"
    )

    schedules: Mapped[list["Schedule"]] = relationship(
        back_populates="student_class"
    )

    def __str__(self):
        return f"{self.year}/{self.symbol}"


# ============================================================
# SCHEDULE
# ============================================================

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    semester: Mapped[str] = mapped_column(String(32))

    student_class_id: Mapped[int] = mapped_column(
        ForeignKey("student_classes.id", ondelete="CASCADE")
    )

    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)

    student_class: Mapped["StudentClass"] = relationship(
        back_populates="schedules"
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="schedule",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"S{self.semester}-{self.student_class}"


class Admin(User):
    __tablename__ = "admins"

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    firstName: Mapped[str] = mapped_column(String(64))
    lastName: Mapped[str] = mapped_column(String(128))
    PESEL: Mapped[str] = mapped_column(String(11), unique=True)
    address: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(255))

# ============================================================
# TEACHER
# ============================================================

class Teacher(User):
    __tablename__ = "teachers"

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    firstName: Mapped[str] = mapped_column(String(64))
    lastName: Mapped[str] = mapped_column(String(128))
    PESEL: Mapped[str] = mapped_column(String(11), unique=True)
    address: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(255))

    formTutor_id: Mapped[int | None] = mapped_column(
        ForeignKey("student_classes.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )

    form_tutor: Mapped["StudentClass | None"] = relationship(
        back_populates="homeroom_teacher"
    )

    subjects: Mapped[list["Subject"]] = relationship(
        back_populates="teacher"
    )

    substitutions_as_replacement: Mapped[list["Substitution"]] = relationship(
        back_populates="substitute_teacher",
        foreign_keys="Substitution.substituteTeacher_id",
    )

    substitutions_as_absent: Mapped[list["Substitution"]] = relationship(
        back_populates="teacher_substituted_for",
        foreign_keys="Substitution.teacherSubstitutedFor_id",
    )

    conduct_entries: Mapped[list["ConductEntry"]] = relationship(
        back_populates="teacher"
    )

    def __str__(self):
        return f"{self.firstName} {self.lastName} - nauczyciel"


# ============================================================
# SUBJECT
# ============================================================

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    hours: Mapped[int] = mapped_column(Integer)

    teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
    )

    studentClass_id: Mapped[int | None] = mapped_column(
        ForeignKey("student_classes.id", ondelete="SET NULL"),
        nullable=True,
    )

    teacher: Mapped["Teacher | None"] = relationship(
        back_populates="subjects"
    )

    student_class: Mapped["StudentClass | None"] = relationship(
        back_populates="subjects"
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="subject"
    )

    grades: Mapped[list["Grade"]] = relationship(
        back_populates="subject"
    )

    presences: Mapped[list["Presence"]] = relationship(
        back_populates="subject"
    )

    substitutions: Mapped[list["Substitution"]] = relationship(
        back_populates="subject"
    )

    def __str__(self):
        return self.name


# ============================================================
# SUBSTITUTION
# ============================================================

class Substitution(Base):
    __tablename__ = "substitutions"

    id: Mapped[int] = mapped_column(primary_key=True)

    substituteTeacher_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
    )

    teacherSubstitutedFor_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
    )

    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE")
    )

    substitute_teacher: Mapped["Teacher | None"] = relationship(
        back_populates="substitutions_as_replacement",
        foreign_keys=[substituteTeacher_id],
    )

    teacher_substituted_for: Mapped["Teacher | None"] = relationship(
        back_populates="substitutions_as_absent",
        foreign_keys=[teacherSubstitutedFor_id],
    )

    subject: Mapped["Subject"] = relationship(
        back_populates="substitutions"
    )

    def __str__(self):
        return (
            f"{self.substitute_teacher} -> "
            f"{self.teacher_substituted_for} - "
            f"{self.date_from}/{self.date_to}"
        )


# ============================================================
# LESSON
# ============================================================

class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)

    subject_id: Mapped[int | None] = mapped_column(
        ForeignKey("subjects.id", ondelete="SET NULL"),
        nullable=True,
    )

    theme: Mapped[str] = mapped_column(String(256))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    dateTimeFrom: Mapped[datetime] = mapped_column(DateTime)
    dateTimeTo: Mapped[datetime] = mapped_column(DateTime)

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE")
    )

    subject: Mapped["Subject | None"] = relationship(
        back_populates="lessons"
    )

    schedule: Mapped["Schedule"] = relationship(
        back_populates="lessons"
    )

    presence_records: Mapped[list["Presence"]] = relationship(
        back_populates="lesson"
    )

    quiz: Mapped["Quiz | None"] = relationship(
        back_populates="lesson",
        uselist=False,
    )

    def __str__(self):
        return f"{self.subject} - {self.dateTimeFrom.date()}/{self.dateTimeFrom.time()}"


# ============================================================
# PARENT
# ============================================================

class Parent(User):
    __tablename__ = "parents"

    __mapper_args__ = {
        "polymorphic_identity": "parent",
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    firstName: Mapped[str] = mapped_column(String(64))
    lastName: Mapped[str] = mapped_column(String(128))
    PESEL: Mapped[str] = mapped_column(String(11), unique=True)
    email: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(256))

    students: Mapped[list["Student"]] = relationship(
        back_populates="parent"
    )

    def __str__(self):
        return f"{self.firstName} {self.lastName} - rodzic"


# ============================================================
# STUDENT
# ============================================================

class Student(User):
    __tablename__ = "students"

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    student_id: Mapped[str] = mapped_column(String(32), unique=True)
    firstName: Mapped[str] = mapped_column(String(64))
    lastName: Mapped[str] = mapped_column(String(128))
    PESEL: Mapped[str] = mapped_column(String(11), unique=True)
    email: Mapped[str] = mapped_column(String(255))
    dateOfBirth: Mapped[date] = mapped_column(Date)

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("parents.id", ondelete="SET NULL"),
        nullable=True,
    )

    address: Mapped[str] = mapped_column(String(256))

    studentClass_id: Mapped[int] = mapped_column(
        ForeignKey("student_classes.id", ondelete="RESTRICT")
    )

    parent: Mapped["Parent | None"] = relationship(
        back_populates="students"
    )

    student_class: Mapped["StudentClass"] = relationship(
        back_populates="students"
    )

    grades: Mapped[list["Grade"]] = relationship(
        back_populates="student"
    )

    presences: Mapped[list["Presence"]] = relationship(
        back_populates="student"
    )

    conduct_entries: Mapped[list["ConductEntry"]] = relationship(
        back_populates="student"
    )

    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.student_class}"


# ============================================================
# GRADE
# ============================================================

class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(256))

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="RESTRICT")
    )

    date_of_issue: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    student: Mapped["Student"] = relationship(
        back_populates="grades"
    )

    subject: Mapped["Subject"] = relationship(
        back_populates="grades"
    )

    def __str__(self):
        return f"{self.value} - {self.subject} - {self.description}"


# ============================================================
# PRESENCE
# ============================================================

class Presence(Base):
    __tablename__ = "presences"

    id: Mapped[int] = mapped_column(primary_key=True)
    present: Mapped[bool] = mapped_column(Boolean, default=True)
    excused: Mapped[bool] = mapped_column(Boolean, default=False)

    date_of_issue: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE")
    )

    student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.id", ondelete="SET NULL"),
        nullable=True,
    )

    lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
    )

    subject: Mapped["Subject"] = relationship(
        back_populates="presences"
    )

    student: Mapped["Student | None"] = relationship(
        back_populates="presences"
    )

    lesson: Mapped["Lesson | None"] = relationship(
        back_populates="presence_records"
    )

    def __str__(self):
        return f"{self.student} - {self.present}"


# ============================================================
# CONDUCT ENTRY
# ============================================================

class ConductEntry(Base):
    __tablename__ = "conduct_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(256))

    type_of_entry: Mapped[ConductEntryType] = mapped_column(
        SQLAlchemyEnum(
            ConductEntryType,
            native_enum=False,
            values_callable=lambda enum: [e.value for e in enum],
            length=3,
        ),
        default=ConductEntryType.NEUTRAL,
    )

    points: Mapped[int] = mapped_column(Integer, default=0)

    date_of_issue: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.id", ondelete="SET NULL"),
        nullable=True,
    )

    teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
    )

    student: Mapped["Student | None"] = relationship(
        back_populates="conduct_entries"
    )

    teacher: Mapped["Teacher | None"] = relationship(
        back_populates="conduct_entries"
    )

    def __str__(self):
        return f"{self.student} - {self.message}"


# ============================================================
# MESSAGE
# ============================================================

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    theme: Mapped[str] = mapped_column(String(256))
    message: Mapped[str] = mapped_column(String(1024))

    date_of_issue: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    sender_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    visible_for_sender: Mapped[bool] = mapped_column(Boolean, default=True)

    receiver_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    visible_for_receiver: Mapped[bool] = mapped_column(Boolean, default=True)

    sender: Mapped["User | None"] = relationship(
        foreign_keys=[sender_id]
    )

    receiver: Mapped["User | None"] = relationship(
        foreign_keys=[receiver_id]
    )


# ============================================================
# PRINCIPAL
# ============================================================

class Principal(User):
    __tablename__ = "principals"

    __mapper_args__ = {
        "polymorphic_identity": "principal",
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    firstName: Mapped[str] = mapped_column(String(64))
    lastName: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(255))
    PESEL: Mapped[str] = mapped_column(String(11), unique=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName} - dyrektor"


# ============================================================
# WORKER
# ============================================================

class Worker(User):
    __tablename__ = "workers"

    __mapper_args__ = {
        "polymorphic_identity": "worker",
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    firstName: Mapped[str] = mapped_column(String(64))
    lastName: Mapped[str] = mapped_column(String(128))
    PESEL: Mapped[str] = mapped_column(String(11), unique=True)
    email: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(256))
    jobTitle: Mapped[str] = mapped_column(String(128))

    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.jobTitle}"


# ============================================================
# QUIZ
# ============================================================

class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))

    type: Mapped[QuizType] = mapped_column(
        SQLAlchemyEnum(
            QuizType,
            native_enum=False,
            values_callable=lambda enum: [e.value for e in enum],
            length=128,
        ),
        default=QuizType.TEST,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="NO ACTION"),
        unique=True,
    )

    lesson: Mapped["Lesson"] = relationship(
        back_populates="quiz"
    )
