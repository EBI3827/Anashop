# Generated by Django 3.0.6 on 2020-06-12 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_wishitem_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='test'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='test'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(default='test'),
        ),
    ]