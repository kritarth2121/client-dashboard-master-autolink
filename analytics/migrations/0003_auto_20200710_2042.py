# Generated by Django 2.2.13 on 2020-07-10 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20200710_1736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='users',
            new_name='client',
        ),
        migrations.AddField(
            model_name='work',
            name='description',
            field=models.TextField(default='YA', max_length=1000),
            preserve_default=False,
        ),
    ]
