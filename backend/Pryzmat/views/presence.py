from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import PresenceSerializer
from Pryzmat.models import Presence

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class PresenceView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet):
    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer    
    permission_classes = [DjangoModelPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(subject__teacher=teacher) | Q(student__studentClass__homeroomTeacher=teacher)).distinct()

    def filter_for_parent(self, qs, parent):
        return qs.filter(student__parent=parent)

    def filter_for_student(self, qs, student):
        return qs.filter(student=student)
    
