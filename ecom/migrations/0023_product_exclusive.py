# Generated by Django 5.1.3 on 2024-12-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0022_product_feautered_priority_product_popular_priority_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='exclusive',
            field=models.BooleanField(default=False, help_text='Select this product to display exclusively'),
        ),
    ]
