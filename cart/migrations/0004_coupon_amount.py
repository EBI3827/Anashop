# Generated by Django 3.0.6 on 2020-07-03 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
    ]
