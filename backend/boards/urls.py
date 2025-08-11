from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import BoardViewSet

router = routers.DefaultRouter()  # paréntesis importantes
router.register(r"board", BoardViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]