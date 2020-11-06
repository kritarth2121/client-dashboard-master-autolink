# Generated by Django 2.2.2 on 2020-07-21 16:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0015_note_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='work',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='work',
            name='assigned_user',
        ),
        migrations.AddField(
            model_name='work',
            name='assigned_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
