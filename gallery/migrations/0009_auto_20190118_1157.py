# Generated by Django 2.1.5 on 2019-01-18 09:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_album_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='modification_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='lens',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='photo',
            name='make',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='photo',
            name='model',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]