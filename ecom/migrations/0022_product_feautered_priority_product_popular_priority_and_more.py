# Generated by Django 5.1.3 on 2024-12-23 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0021_delete_payment_product_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='feautered_priority',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='product',
            name='popular_priority',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='priority',
            field=models.IntegerField(default=1000),
        ),
    ]
