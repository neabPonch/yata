# Generated by Django 3.0.1 on 2020-03-03 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faction', '0061_auto_20200302_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='attackchain',
            name='code',
            field=models.SlugField(default='0', max_length=32),
        ),
        migrations.AddField(
            model_name='attackreport',
            name='code',
            field=models.SlugField(default='0', max_length=32),
        ),
    ]
