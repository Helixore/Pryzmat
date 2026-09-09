from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from Pryzmat.serializers import SubjectSerializer
from Pryzmat.models import Subject

class SubjectView(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    
    permission_classes = [DjangoObjectPermissions]
    