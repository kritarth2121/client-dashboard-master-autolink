# Generated by Django 2.2.6 on 2020-08-01 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0027_auto_20200801_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='comment',
        ),
    ]
