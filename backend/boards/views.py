from django.shortcuts import render
from rest_framework import viewset
from .serializer import BoardSerializer
from .models import Board

# Create your views here.

class BoardViewSet(viewset.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer