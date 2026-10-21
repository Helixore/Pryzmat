from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import MessageSerializer
from Pryzmat.models import Message

from Pryzmat.lib.mixins import RoleFilteredQuerysetMixin
from Pryzmat.lib.permissions import IsTeacherOrPrincipal

class MessageView(RoleFilteredQuerysetMixin, viewsets.ModelViewSet): #received messages; TODO: view sent messages
    queryset = Message.objects.all()
    serializer_class = MessageSerializer    
    permission_classes = [DjangoModelPermissions]
    
    def filter_for_teacher(self, qs, teacher):
        # oceny wystawione przez niego LUB jego wychowanków (klasa, której jest wychowawcą)
        return qs.filter(Q(receiver=teacher.user)).distinct()

    def filter_for_parent(self, qs, parent):
        children = parent.student_set.all()
        message_ids = children.values_list("user", flat=True)
        return qs.filter(Q(receiver=parent.user) | Q(receiver__in=message_ids))

    def filter_for_student(self, qs, student):
        return qs.filter(receiver=student.user)
    
