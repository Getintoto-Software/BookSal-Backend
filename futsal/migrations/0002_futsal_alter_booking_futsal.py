# Generated by Django 5.1.1 on 2024-12-11 06:18

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futsal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Futsal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('futsal_name', models.CharField(max_length=200)),
                ('futsal_image_1', models.ImageField(upload_to='images/futsal_images/')),
                ('futsal_image_2', models.ImageField(blank=True, null=True, upload_to='images/futsal_images/')),
                ('futsal_image_3', models.ImageField(blank=True, null=True, upload_to='images/futsal_images/')),
                ('futsal_image_4', models.ImageField(blank=True, null=True, upload_to='images/futsal_images/')),
                ('futsal_image_5', models.ImageField(blank=True, null=True, upload_to='images/futsal_images/')),
                ('location', models.CharField(max_length=400)),
                ('google_maps_link', models.URLField(blank=True, null=True)),
                ('a_side', models.CharField(max_length=10)),
                ('grounds', models.IntegerField()),
                ('shower_facility', models.BooleanField(default=False)),
                ('parking_space', models.BooleanField(default=False)),
                ('changing_room', models.BooleanField(default=False)),
                ('restaurant', models.BooleanField(default=False)),
                ('wifi', models.BooleanField(default=False)),
                ('futsal_description', models.TextField(default='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('futsal_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='futsal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futsal.futsal'),
        ),
    ]
