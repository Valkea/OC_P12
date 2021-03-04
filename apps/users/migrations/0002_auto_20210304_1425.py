# Generated by Django 3.1.7 on 2021-03-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="epicmember",
            name="team",
            field=models.CharField(
                choices=[
                    ("MANAGE", "Managing team"),
                    ("SELL", "Sales team"),
                    ("SUPPORT", "Support team"),
                    ("NONE", "Need a team"),
                ],
                default="NONE",
                max_length=10,
                verbose_name="Status",
            ),
        ),
    ]