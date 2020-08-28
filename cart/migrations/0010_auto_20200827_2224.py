# Generated by Django 3.0.6 on 2020-08-27 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0009_auto_20200706_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkoutinfo', to=settings.AUTH_USER_MODEL),
        ),
    ]
