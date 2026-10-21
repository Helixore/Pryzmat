from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import SubstitutionSerializer
from Pryzmat.models import Substitution

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class SubstitutionView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Substitution.objects.all()
    serializer_class = SubstitutionSerializer    
    permission_classes = [DjangoModelPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(teacherSubstitutedFor=teacher) | Q(teacherSubstitutedFor__subject__studentClass__homeroomTeacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(teacherSubstitutedFor__subject__studentClass__student__parent=parent)

    def filter_for_student(self, qs, student):
        return qs.filter(teacherSubstitutedFor__subject__studentClass__student=student)
    
