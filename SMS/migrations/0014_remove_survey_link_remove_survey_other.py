# Generated by Django 4.0.6 on 2023-12-15 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0013_remove_all_campaign_whitelist_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='link',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='other',
        ),
    ]