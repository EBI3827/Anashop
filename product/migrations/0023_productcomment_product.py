# Generated by Django 3.0.6 on 2020-06-25 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_remove_productcomment_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product.Product'),
        ),
    ]