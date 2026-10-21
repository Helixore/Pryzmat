from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import ScheduleSerializer
from Pryzmat.models import Schedule

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class ScheduleView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
    permission_classes = [DjangoModelPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(studentClass=teacher.formTutor) | Q(studentClass__subject__teacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        children = parent.student_set.all()
        class_ids = children.values_list("studentClass", flat=True)
        return qs.filter(studentClass__in=class_ids)

    def filter_for_student(self, qs, student):
        return qs.filter(studentClass=student.studentClass)