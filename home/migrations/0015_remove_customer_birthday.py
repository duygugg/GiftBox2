# Generated by Django 3.1.3 on 2021-01-10 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20210110_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='birthday',
        ),
    ]
