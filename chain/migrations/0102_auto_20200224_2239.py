# Generated by Django 3.0.1 on 2020-02-24 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0101_auto_20200116_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attack',
            name='breakdown',
        ),
        migrations.RemoveField(
            model_name='attacks',
            name='report',
        ),
        migrations.RemoveField(
            model_name='attacksbreakdown',
            name='faction',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='report',
        ),
        migrations.RemoveField(
            model_name='chain',
            name='faction',
        ),
        migrations.RemoveField(
            model_name='count',
            name='report',
        ),
        migrations.RemoveField(
            model_name='crontab',
            name='faction',
        ),
        migrations.DeleteModel(
            name='FactionData',
        ),
        migrations.RemoveField(
            model_name='member',
            name='faction',
        ),
        migrations.DeleteModel(
            name='Racket',
        ),
        migrations.RemoveField(
            model_name='report',
            name='chain',
        ),
        migrations.RemoveField(
            model_name='revive',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='revivecontract',
            name='faction',
        ),
        migrations.RemoveField(
            model_name='stat',
            name='faction',
        ),
        migrations.DeleteModel(
            name='Territory',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='factions',
        ),
        migrations.DeleteModel(
            name='Attack',
        ),
        migrations.DeleteModel(
            name='Attacks',
        ),
        migrations.DeleteModel(
            name='AttacksBreakdown',
        ),
        migrations.DeleteModel(
            name='Bonus',
        ),
        migrations.DeleteModel(
            name='Chain',
        ),
        migrations.DeleteModel(
            name='Count',
        ),
        migrations.DeleteModel(
            name='Crontab',
        ),
        migrations.DeleteModel(
            name='Faction',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.DeleteModel(
            name='Revive',
        ),
        migrations.DeleteModel(
            name='ReviveContract',
        ),
        migrations.DeleteModel(
            name='Stat',
        ),
        migrations.DeleteModel(
            name='Wall',
        ),
    ]