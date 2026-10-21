from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import TeacherSerializer
from Pryzmat.models import Teacher

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class TeacherView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer    
    permission_classes = [DjangoModelPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        return qs.filter(Q(teacher=teacher) | Q(student__homeroom_teacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(subject__studentClass__student__parent=parent).distinct()

    def filter_for_student(self, qs, student):
        studentClass = student.studentClass
        subjects = studentClass.subject_set.all()
        teacher_ids = subjects.values_list("teacher", flat=True)
        return qs.filter(id__in=teacher_ids)
    
