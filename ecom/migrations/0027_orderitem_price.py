# Generated by Django 5.1.3 on 2025-01-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0026_order_delivery_fee_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
