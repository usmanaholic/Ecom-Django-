# Generated by Django 5.1.3 on 2024-11-23 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0007_product_popular_product_recent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='recent',
        ),
    ]