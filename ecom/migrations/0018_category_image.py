# Generated by Django 5.1.3 on 2024-12-08 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0017_herosectionimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]