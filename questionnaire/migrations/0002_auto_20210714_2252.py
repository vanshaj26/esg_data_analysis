# Generated by Django 3.2.5 on 2021-07-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_model',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='question_model',
            name='unit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]