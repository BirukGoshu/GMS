# Generated by Django 4.0.6 on 2024-01-27 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0020_alter_all_campaign_whitelist_customer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMStype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='all_campaign_whitelist',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.smstype'),
        ),
        migrations.AddField(
            model_name='all_campaigns',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.smstype'),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.smstype'),
        ),
        migrations.AddField(
            model_name='survey',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.smstype'),
        ),
    ]