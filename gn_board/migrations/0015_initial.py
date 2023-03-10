# Generated by Django 4.1.5 on 2023-01-12 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gn_board.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('title', models.CharField(max_length=20, null=True)),
                ('content', models.TextField(null=True)),
                ('list_num', models.AutoField(primary_key=True, serialize=False)),
                ('board_time', models.DateField(auto_now_add=True)),
                ('upload_files', models.FileField(blank=True, null=True, upload_to=gn_board.models.get_file_path, verbose_name='파일')),
                ('filename', models.CharField(max_length=64, null=True, verbose_name='첨부파일명')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
