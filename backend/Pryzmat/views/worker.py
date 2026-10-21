from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import WorkerSerializer
from Pryzmat.models import Worker

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class WorkerView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer    
    permission_classes = [DjangoModelPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs

    def filter_for_parent(self, qs, parent):
        return qs

    def filter_for_student(self, qs, student):
        return qs
    
