# Generated by Django 4.0.6 on 2023-12-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0009_rename_service_id_all_campaign_whitelist_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='template',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='all_campaigns',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='all_campaigns',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
