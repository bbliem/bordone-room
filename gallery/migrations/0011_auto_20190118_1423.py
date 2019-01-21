# Generated by Django 2.1.5 on 2019-01-18 12:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0010_auto_20190118_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='album',
            name='modification_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]