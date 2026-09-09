from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import StudentClassSerializer
from Pryzmat.models import StudentClass

class StudentClassView(viewsets.ModelViewSet):
    serializer_class = StudentClassSerializer
    queryset = StudentClass.objects.all()
    
    permission_classes = [DjangoModelPermissions]
    