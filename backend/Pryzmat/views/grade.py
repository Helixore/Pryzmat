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
    
    permission_classes = [DjangoObjectPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(subject__teacher=teacher) | Q(student__studentClass__homeroomTeacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(student__parent=parent)

    def filter_for_student(self, qs, student):
        return qs.filter(student=student)
    