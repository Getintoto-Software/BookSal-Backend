# Generated by Django 5.1.1 on 2025-04-10 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='featured_status',
            field=models.BooleanField(default=False),
        ),
    ]
