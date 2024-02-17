# Generated by Django 4.0.6 on 2023-12-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0010_remove_customers_business_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='bussiness_types',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='industries',
        ),
        migrations.AddField(
            model_name='customers',
            name='business_type',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='industry',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
    ]