# Generated by Django 3.2.9 on 2021-11-21 19:29

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(max_length=50)),
                ('team2', models.CharField(max_length=50)),
                ('odds1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('odds2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dateTimeStamp', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now)),
                ('site', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
