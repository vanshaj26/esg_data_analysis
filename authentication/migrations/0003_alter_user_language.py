# Generated by Django 3.2.5 on 2021-07-19 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        ('authentication', '0002_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_lang', to='language.language'),
        ),
    ]