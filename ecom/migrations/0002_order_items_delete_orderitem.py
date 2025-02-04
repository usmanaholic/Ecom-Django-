# Generated by Django 5.1.3 on 2025-01-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.JSONField(default=list, help_text="List of items, e.g., [{'product_id': 1, 'quantity': 2, 'price': 100.00}, ...]"),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
