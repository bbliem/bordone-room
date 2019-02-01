# Generated by Django 2.1.5 on 2019-02-01 16:24

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import gallery.models
import gallery.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='title', unique=True)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modification_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='name', unique=True)),
                ('description', models.TextField()),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('public', models.BooleanField(default=False)),
                ('original', models.ImageField(storage=gallery.storage.PhotoStorage(), upload_to=gallery.models.original_path)),
                ('date_taken', models.DateTimeField(blank=True, null=True)),
                ('make', models.CharField(blank=True, default='', max_length=200)),
                ('model', models.CharField(blank=True, default='', max_length=200)),
                ('lens', models.CharField(blank=True, default='', max_length=200)),
                ('aperture', models.FloatField(blank=True, null=True)),
                ('focal_length', models.FloatField(blank=True, null=True)),
                ('shutter_speed', models.FloatField(blank=True, null=True)),
                ('iso', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='gallery.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='gallery.Photo'),
        ),
    ]
