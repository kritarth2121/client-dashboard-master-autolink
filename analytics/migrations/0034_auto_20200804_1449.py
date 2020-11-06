# Generated by Django 2.2.6 on 2020-08-04 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0033_auto_20200803_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='subtask',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='work',
            name='assigned_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Staff members '),
        ),
        migrations.AlterField(
            model_name='work',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
