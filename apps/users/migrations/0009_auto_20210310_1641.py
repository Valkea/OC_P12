# Generated by Django 3.1.7 on 2021-03-10 16:41

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_auto_20210310_1543"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="epicmember",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name="epicmember",
            name="password",
            field=models.CharField(max_length=100, null=True, verbose_name="Password"),
        ),
    ]
