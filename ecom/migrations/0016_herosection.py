# Generated by Django 5.1.3 on 2024-12-08 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0015_product_free_delivery_alter_product_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Discover Your Next Favorite Product', max_length=200)),
                ('description', models.TextField(default='Shop our latest collections and exclusive offers')),
                ('button_text', models.CharField(default='Shop Now', max_length=50)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='hero_images/')),
            ],
        ),
    ]