# Generated by Django 2.2.6 on 2020-07-30 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0025_auto_20200729_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Start'), ('progress', 'In Progress'), ('pendingreview', 'Pending for Review'), ('feedback', 'Client Feedback'), ('completed', 'Completed')], default='Pending Start', max_length=20),
        ),
    ]
