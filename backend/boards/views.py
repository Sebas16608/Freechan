from django.shortcuts import render
from .serializers import BoardSerializer
from .models import Board
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
