# Generated by Django 5.1.1 on 2025-02-01 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_rename_changing_room_userprofile_is_futsal_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
