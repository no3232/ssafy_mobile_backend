# Generated by Django 3.2.13 on 2023-01-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20230128_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=50),
        ),
    ]
