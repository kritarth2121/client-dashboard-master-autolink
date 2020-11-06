# Generated by Django 2.2.2 on 2020-07-22 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0018_auto_20200722_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuetrack',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects_issue', to='analytics.Project'),
        ),
        migrations.AddField(
            model_name='issuetrack',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works_issue', to='analytics.Work'),
        ),
    ]
