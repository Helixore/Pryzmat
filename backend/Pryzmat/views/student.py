from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from Pryzmat.serializers import StudentSerializer
from Pryzmat.models import Student

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class StudentView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [DjangoObjectPermissions]
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(studentClass__subject__teacher=teacher) | Q(studentClass__homeroomTeacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(parent=parent)

    def filter_for_student(self, qs, student):
        return qs.filter(student_id=student.student_id)