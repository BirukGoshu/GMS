# Generated by Django 4.0.6 on 2023-12-14 08:45

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0005_alter_customer_phones_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=15)),
                ('age', models.IntegerField()),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='ET')),
                ('phonetype', models.CharField(choices=[('smart', 'Smart Phone'), ('non-smart', 'non-smart Phone')], default='smart', max_length=15)),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='UserManagment.industries')),
            ],
            options={
                'db_table': 'subscribers',
            },
        ),
    ]