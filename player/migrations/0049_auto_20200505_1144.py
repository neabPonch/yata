# Generated by Django 3.0.4 on 2020-05-05 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0048_trainfull_req'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='awardsInfo',
        ),
        migrations.RemoveField(
            model_name='player',
            name='awardsJson',
        ),
        migrations.AddField(
            model_name='player',
            name='awardsNumb',
            field=models.IntegerField(default=0),
        ),
    ]