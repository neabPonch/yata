# Generated by Django 2.2.7 on 2019-12-02 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_configuration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BotData',
        ),
        migrations.RemoveField(
            model_name='preference',
            name='player',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Preference',
        ),
    ]
