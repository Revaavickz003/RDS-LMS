# Generated by Django 5.1.2 on 2024-10-17 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_alter_lead_client_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='timestamp',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 10, 17, 22, 13, 36, 736662)),
        ),
    ]
