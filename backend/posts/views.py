from django.shortcuts import render
from .serializers import PostSerializer
from .models import Post
from rest_framework import viewsets
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer