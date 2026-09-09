from django.contrib import admin
from .models import StudentClass, Schedule, Teacher, Subject, Substitution, Lesson, Parent, Student, Grade, Presence, ConductEntry, Message, Principal, Worker

# Register your models here.
admin.site.register(StudentClass)
admin.site.register(Schedule)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Substitution)
admin.site.register(Lesson)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Grade)
admin.site.register(Presence)
admin.site.register(ConductEntry)
admin.site.register(Message)
admin.site.register(Principal)
admin.site.register(Worker)
