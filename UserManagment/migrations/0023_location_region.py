# Generated by Django 4.0.6 on 2024-02-15 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0022_alter_customers_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
