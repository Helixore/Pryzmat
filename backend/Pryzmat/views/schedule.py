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
    permission_classes = [DjangoModelPermissions, IsTeacherOrPrincipal]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(teacher=teacher) | Q(student__homeroom_teacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(student__parents=parent)

    def filter_for_student(self, qs, student):
        return qs.filter(student=student)