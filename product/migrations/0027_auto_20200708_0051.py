# Generated by Django 3.0.6 on 2020-07-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_productcomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ip',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='session',
            field=models.CharField(max_length=40, null=True),
        ),
    ]