# Generated by Django 4.0.6 on 2023-12-14 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0006_subscribers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SMS', '0003_alter_all_campaigns_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='only_data_campaigns',
            name='customer',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='all_campaigns',
            name='phones',
            field=models.FileField(null=True, upload_to='content/Phones'),
        ),
        migrations.CreateModel(
            name='all_campaign_whitelist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True)),
                ('link', models.CharField(max_length=50)),
                ('sender', models.CharField(max_length=50)),
                ('phones', models.FileField(blank=True, null=True, upload_to='all_campaign_whitelist/Phones/')),
                ('message', models.TextField()),
                ('other', models.CharField(max_length=20)),
                ('age', models.CharField(blank=True, max_length=191, null=True)),
                ('expected_delivery', models.CharField(blank=True, max_length=191, null=True)),
                ('gender', models.CharField(blank=True, max_length=191, null=True)),
                ('phone_type', models.CharField(blank=True, max_length=191, null=True)),
                ('date_tobe_sent', models.DateTimeField(null=True)),
                ('location', models.CharField(blank=True, max_length=191, null=True)),
                ('occupation', models.CharField(blank=True, max_length=191, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('approved', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('service_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='UserManagment.services')),
            ],
            options={
                'db_table': 'whitelist_all_campaign',
            },
        ),
    ]
