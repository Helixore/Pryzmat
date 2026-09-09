'''
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from Pryzmat.serializers import WorkerSerializer
from Pryzmat.models import Worker

class WorkerView(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    
    permission_classes = [DjangoModelPermissions]
    '''