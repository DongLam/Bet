# Generated by Django 3.2.9 on 2021-11-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20211121_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='dateTimeStamp',
            field=models.DateTimeField(blank=True),
        ),
    ]
