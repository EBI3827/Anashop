# Generated by Django 3.0.6 on 2020-08-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_hit'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='category/'),
        ),
    ]