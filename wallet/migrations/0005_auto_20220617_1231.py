# Generated by Django 3.1 on 2022-06-17 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_auto_20220614_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 12, 31, 16, 271799)),
        ),
    ]
