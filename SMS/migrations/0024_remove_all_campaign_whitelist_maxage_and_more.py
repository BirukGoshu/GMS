# Generated by Django 4.0.6 on 2024-02-02 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0023_remove_all_campaign_whitelist_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_campaign_whitelist',
            name='maxage',
        ),
        migrations.RemoveField(
            model_name='all_campaign_whitelist',
            name='maxsmsexpected',
        ),
        migrations.RemoveField(
            model_name='all_campaign_whitelist',
            name='minage',
        ),
        migrations.RemoveField(
            model_name='all_campaign_whitelist',
            name='minsmsexpected',
        ),
        migrations.RemoveField(
            model_name='only_data_campaigns',
            name='maxage',
        ),
        migrations.RemoveField(
            model_name='only_data_campaigns',
            name='maxsmsexpected',
        ),
        migrations.RemoveField(
            model_name='only_data_campaigns',
            name='minage',
        ),
        migrations.RemoveField(
            model_name='only_data_campaigns',
            name='minsmsexpected',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='maxage',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='maxsmsexpected',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='minage',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='minsmsexpected',
        ),
    ]
