from django.urls import path, include
from .views import ThreadViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"thread", ThreadViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]