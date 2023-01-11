from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    list_num = models.AutoField(primary_key=True)
    board_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
