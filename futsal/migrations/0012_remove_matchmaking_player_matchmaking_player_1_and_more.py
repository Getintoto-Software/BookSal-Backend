# Generated by Django 5.1.1 on 2025-02-05 07:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futsal', '0011_alter_matchmaking_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchmaking',
            name='player',
        ),
        migrations.AddField(
            model_name='matchmaking',
            name='player_1',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='player_1', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matchmaking',
            name='player_2',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='player_2', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
