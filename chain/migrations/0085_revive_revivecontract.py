# Generated by Django 3.0.1 on 2020-01-04 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0084_auto_20191229_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviveContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField(default=0)),
                ('end', models.IntegerField(default=0)),
                ('computing', models.BooleanField(default=0)),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chain.Faction')),
            ],
        ),
        migrations.CreateModel(
            name='Revive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField(default=0)),
                ('reviver_id', models.IntegerField(default=0)),
                ('reviver_name', models.CharField(default='reviver_name', max_length=32)),
                ('reviver_faction', models.IntegerField(default=0)),
                ('reviver_factionname', models.CharField(blank=True, default='reviver_factionname', max_length=32, null=True)),
                ('target_id', models.IntegerField(default=0)),
                ('target_name', models.CharField(default='target_name', max_length=32)),
                ('target_faction', models.IntegerField(default=0)),
                ('target_factionname', models.CharField(blank=True, default='target_factionname', max_length=32, null=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chain.ReviveContract')),
            ],
        ),
    ]