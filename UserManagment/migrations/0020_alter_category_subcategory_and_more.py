# Generated by Django 4.0.6 on 2024-02-02 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0019_location_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subcategory',
            field=models.ManyToManyField(blank=True, to='UserManagment.subcategories'),
        ),
        migrations.AlterField(
            model_name='package_subscriptions',
            name='options',
            field=models.ManyToManyField(blank=True, to='UserManagment.subcategories'),
        ),
    ]