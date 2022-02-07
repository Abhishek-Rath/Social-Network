# Generated by Django 3.0 on 2022-02-07 20:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20220207_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(default=None, related_name='users_who_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
