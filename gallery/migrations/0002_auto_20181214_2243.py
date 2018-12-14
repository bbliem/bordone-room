# Generated by Django 2.1.4 on 2018-12-14 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='aperture',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_taken',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='focal_length',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='iso',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='shut_denom',
            field=models.IntegerField(blank=True, null=True, verbose_name='shutter speed denominator'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='shut_numer',
            field=models.IntegerField(blank=True, null=True, verbose_name='shutter speed numerator'),
        ),
    ]
