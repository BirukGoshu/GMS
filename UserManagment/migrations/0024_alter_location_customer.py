# Generated by Django 4.0.6 on 2024-02-16 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0023_location_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customerlocation', to='UserManagment.customers'),
        ),
    ]
