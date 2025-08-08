from django.db import models
from boards.models import Boards
# Create your models here.

class Thread(models.Model):
    board = models.ForeignKey(Boards, on_delete=models.CASCADE, related_name='board')
    