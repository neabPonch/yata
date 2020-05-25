# Generated by Django 3.0.4 on 2020-05-25 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0029_verifiedclient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifiedclient',
            name='author_name',
            field=models.CharField(default='Player', max_length=16),
        ),
        migrations.AlterField(
            model_name='verifiedclient',
            name='name',
            field=models.CharField(default='?', max_length=32),
        ),
        migrations.AlterField(
            model_name='verifiedclient',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='verifiedclient',
            name='version',
            field=models.CharField(default='v0.1', max_length=16),
        ),
    ]
