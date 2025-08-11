from django.shortcuts import render
from .serializers import ThreadSerializer
from rest_framework import viewsets
from .models import Thread

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
