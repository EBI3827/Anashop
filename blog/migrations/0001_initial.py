# Generated by Django 3.0.6 on 2020-07-09 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('composer', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('short_desc', models.TextField()),
                ('blog_data', models.TextField()),
                ('blog_image', models.ImageField(upload_to='blog/')),
            ],
        ),
    ]
