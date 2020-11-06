# Generated by Django 2.2.2 on 2020-07-23 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0021_delete_issuetrack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], default='Medium', max_length=20),
        ),
        migrations.AlterField(
            model_name='work',
            name='priority',
            field=models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], default='Medium', max_length=20),
        ),
    ]