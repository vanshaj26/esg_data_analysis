# Generated by Django 3.2.5 on 2021-07-21 17:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        ('questionnaire', '0003_auto_20210720_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='question_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lang_ques', to='language.language')),
            ],
        ),
        migrations.CreateModel(
            name='ques_cat_mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catego', to='questionnaire.cates')),
                ('framework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame', to='questionnaire.cates')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lang_map', to='language.language')),
                ('ques_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapped_ques', to='questionnaire.question_model')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_cate', to='questionnaire.cates')),
            ],
        ),
    ]