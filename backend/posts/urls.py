from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import PostViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("api/", include(router.urls))
]