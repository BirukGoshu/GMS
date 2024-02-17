# Generated by Django 4.0.6 on 2023-12-22 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagment', '0013_customerfiles_created_at_customerfiles_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='UserManagment.subcategories')),
            ],
        ),
        migrations.AddField(
            model_name='package_subscriptions',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='UserManagment.category'),
        ),
        migrations.AddField(
            model_name='package_subscriptions',
            name='customcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='UserManagment.customcategory'),
        ),
    ]
