# Generated by Django 2.1.5 on 2019-01-26 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0011_auto_20190118_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]