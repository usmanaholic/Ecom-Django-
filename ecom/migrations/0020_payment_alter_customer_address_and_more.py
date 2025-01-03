# Generated by Django 5.1.3 on 2024-12-23 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0019_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='herosection',
            name='title',
            field=models.CharField(default='Discover Your Next Favorite Product', max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(max_length=500, null=True),
        ),
    ]