# Generated by Django 5.0.6 on 2024-06-06 07:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]