from django.db import models
from threads.models import Thread
# Create your models here.

class Posts(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='Thread')
