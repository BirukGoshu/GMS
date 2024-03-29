# Generated by Django 4.0.6 on 2024-02-16 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0023_location_region'),
        ('SMS', '0031_all_campaign_whitelist_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_campaign_whitelist',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagment.location'),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagment.location'),
        ),
    ]
