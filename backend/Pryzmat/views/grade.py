from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from Pryzmat.serializers import GradeSerializer
from Pryzmat.models import Grade

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class GradeView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    
    permission_classes = [DjangoObjectPermissions, IsTeacherOrPrincipal]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(teacher=teacher) | Q(student__homeroom_teacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(student__parents=parent)

    def filter_for_student(self, qs, student):
        return qs.filter(student=student)
    