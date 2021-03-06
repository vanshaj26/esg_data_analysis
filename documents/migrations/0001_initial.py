# Generated by Django 3.2.5 on 2021-07-11 13:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import documents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=100)),
                ('document_description', models.TextField()),
                ('document', models.FileField(upload_to=documents.models.upload_file_path)),
                ('doc_type', models.CharField(choices=[('public', 'public'), ('private', 'private')], max_length=7, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='private_doc_access',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('access_tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ten', to='organisation.tenant')),
                ('doc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='docu', to='documents.documents')),
            ],
        ),
    ]
