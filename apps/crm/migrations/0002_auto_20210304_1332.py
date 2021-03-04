# Generated by Django 3.1.7 on 2021-03-04 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_contact_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_contracts', to='crm.client'),
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_contact_contracts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_contact_clients', to=settings.AUTH_USER_MODEL),
        ),
    ]
