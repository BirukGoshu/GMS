# Generated by Django 4.0.6 on 2024-02-16 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0029_remove_all_campaign_whitelist_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_campaign_whitelist',
            name='location',
        ),
        migrations.RemoveField(
            model_name='demographicsurvey',
            name='location',
        ),
        migrations.RemoveField(
            model_name='only_data_campaigns',
            name='location',
        ),
    ]
