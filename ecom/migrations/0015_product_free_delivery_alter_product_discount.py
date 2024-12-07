# Generated by Django 5.1.3 on 2024-12-05 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0014_order_address_order_email_order_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='free_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(blank=True, help_text='Discount Price', null=True),
        ),
    ]