# Generated by Django 5.1.3 on 2024-11-28 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0008_remove_product_recent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
    ]