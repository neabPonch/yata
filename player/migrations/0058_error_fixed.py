# Generated by Django 3.0.8 on 2020-09-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0057_auto_20200906_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='error',
            name='fixed',
            field=models.BooleanField(default=False),
        ),
    ]