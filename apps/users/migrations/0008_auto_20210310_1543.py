# Generated by Django 3.1.7 on 2021-03-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_auto_20210310_1540"),
    ]

    operations = [
        migrations.AlterField(
            model_name="epicmember",
            name="email",
            field=models.EmailField(
                blank=True, max_length=100, null=True, verbose_name="Email"
            ),
        ),
    ]