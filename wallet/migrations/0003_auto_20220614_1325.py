# Generated by Django 3.1 on 2022-06-14 10:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20220613_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 14, 13, 25, 35, 899624)),
        ),
    ]
