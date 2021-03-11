# Generated by Django 3.1.7 on 2021-03-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_event_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(choices=[('CLIENT', 'Client status'), ('CONTRACT', 'Contract status'), ('EVENT', 'Event status')], default='CLIENT', max_length=10, verbose_name='Table')),
                ('value', models.CharField(max_length=20, verbose_name='Database value')),
                ('label', models.CharField(max_length=100, verbose_name='Displayed value')),
            ],
        ),
    ]
