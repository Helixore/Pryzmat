from django.db import models
from django.contrib.auth.models import User

class ConductEntryType(models.TextChoices):
    POSITIVE = "POS", "Pozytywna"
    NEGATIVE = "NEG", "Negatywna"
    NEUTRAL = "NEU", "Neutralna"

class QuizType(models.TextChoices):
    TEST = "Sprawdzian"
    QUIZ = "Kartkówka"

# Create your models here.

class StudentClass(models.Model):
    year = models.IntegerField()
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.year}/{self.symbol}"

class Schedule(models.Model):
    semester = models.CharField(max_length=32)
    studentClass = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"S{self.semester}-{self.studentClass}"

class Teacher(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=128)
    PESEL = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=256)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    formTutor = models.OneToOneField(StudentClass, on_delete=models.SET_NULL, null=True, blank=True, related_name="homeroomTeacher")
    
    def __str__(self):
        return f"{self.firstName} {self.lastName} - nauczyciel"

class Subject(models.Model):
    name = models.CharField(max_length=32)
    hours = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    studentClass = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.name}"

class Substitution(models.Model):
    substituteTeacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="substitiution_as_replacement")
    teacherSubstitutedFor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="substitiution_as_absent")
    date_from = models.DateField()
    date_to = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.substituteTeacher} -> {self.teacherSubstitutedFor} - {self.date_from}/{self.date_to}"

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    theme = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)
    dateTimeFrom = models.DateTimeField()
    dateTimeTo = models.DateTimeField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.subject} - {self.dateTimeFrom.date()}/{self.dateTimeFrom.time()}"

class Parent(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=128)
    PESEL = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.firstName} {self.lastName} - rodzic"

class Student(models.Model):
    student_id = models.CharField(max_length=32, unique=True)
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=128)
    PESEL = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    dateOfBirth = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=256)
    studentClass = models.ForeignKey(StudentClass, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.studentClass}"

class Grade(models.Model):
    value = models.FloatField()
    description = models.CharField(max_length=256)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.value} - {self.subject} - {self.description}"
    
class Presence(models.Model):
    present = models.BooleanField(default=True)
    excused = models.BooleanField(default=False)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.student} - {self.present}"

class ConductEntry(models.Model):
    message = models.CharField(max_length=256)
    type_of_entry = models.CharField(max_length=3, choices=ConductEntryType.choices, default=ConductEntryType.NEUTRAL)
    points = models.IntegerField(default=0)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.student} - {self.message}"
    
class Message(models.Model):
    theme = models.CharField(max_length=256)
    message = models.CharField(max_length=1024)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    visible_for_sender = models.BooleanField(default=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reciever')
    visible_for_receiver = models.BooleanField(default=True)
    
class Principal(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    email = models.EmailField()
    PESEL = models.CharField(max_length=11, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.firstName} {self.lastName} - dyrektor"
    
class Worker(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=128)
    PESEL = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    jobTitle = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.jobTitle}"
    
class Quiz(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(choices=QuizType.choices, default=QuizType.TEST, max_length=128)
    lesson = models.OneToOneField(Lesson, on_delete=models.DO_NOTHING)
    
    