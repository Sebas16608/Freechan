from django.contrib import admin
from django.urls import path
from rest_framework import routers
from .views import BoardViewSet

router = routers.DefaultRouter()  # paréntesis importantes
router.register(r"board", BoardViewSet)

urlpatterns = [
    path("api/boards/", include(router.url)),
]