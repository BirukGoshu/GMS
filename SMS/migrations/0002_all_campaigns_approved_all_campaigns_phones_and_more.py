# Generated by Django 4.0.6 on 2023-09-12 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0002_alter_users_business_type_alter_users_company_name_and_more'),
        ('SMS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_campaigns',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='all_campaigns',
            name='phones',
            field=models.FileField(null=True, upload_to='UserManagment/uploads/Phones'),
        ),
        migrations.AddField(
            model_name='all_campaigns',
            name='sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='age',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='app_models_user',
            field=models.PositiveBigIntegerField(db_column='App\\Models\\User', null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='campaign_name',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='date_tobe_sent',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='expected_delivery',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='gender',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='location',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='occupation',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='phone_type',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='ref_number',
            field=models.CharField(max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='service_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='UserManagment.services'),
        ),
        migrations.AddField(
            model_name='only_data_campaigns',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='all_campaigns',
            name='service_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='UserManagment.services'),
        ),
        migrations.AlterField(
            model_name='all_campaigns',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterModelTable(
            name='only_data_campaigns',
            table='only_data_campaigns',
        ),
    ]
