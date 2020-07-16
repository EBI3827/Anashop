# Generated by Django 3.0.6 on 2020-07-07 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20200708_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='product',
            name='session',
        ),
        migrations.CreateModel(
            name='ProductView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productviews', to='product.Product')),
            ],
        ),
    ]
