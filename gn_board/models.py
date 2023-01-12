from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4
from datetime import datetime

# Create your models here.
def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])



class Board(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    list_num = models.AutoField(primary_key=True)
    board_time = models.DateField(auto_now_add=True)
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')


