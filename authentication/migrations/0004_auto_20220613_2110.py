# Generated by Django 3.1 on 2022-06-13 18:10

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20220613_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 18, 10, 17, 979912)),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(db_index=True, max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format         +256706626855. Up to 10 digits allowed.', regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 18, 10, 17, 979912)),
        ),
    ]
