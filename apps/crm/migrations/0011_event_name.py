# Generated by Django 3.1.7 on 2021-03-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0010_auto_20210304_1706"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="name",
            field=models.CharField(
                default="demo event", max_length=250, verbose_name="Event name"
            ),
            preserve_default=False,
        ),
    ]