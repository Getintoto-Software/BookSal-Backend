# Generated by Django 5.1.1 on 2025-04-10 10:34

import autoslug.fields
import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', autoslug.fields.AutoSlugField(editable=False, populate_from='name', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', autoslug.fields.AutoSlugField(editable=False, populate_from='title', primary_key=True, serialize=False, unique=True)),
                ('meta_tags', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True)),
                ('author', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.category')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
