# Generated by Django 4.0.6 on 2024-02-17 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0035_all_campaign_whitelist_totalphones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='only_data_campaigns',
            name='maxage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='minage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]