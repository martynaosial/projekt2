# Generated by Django 5.1.2 on 2025-01-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder_apki', '0005_product_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('adminki', 'Administrator'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
