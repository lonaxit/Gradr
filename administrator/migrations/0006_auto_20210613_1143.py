# Generated by Django 3.2 on 2021-06-13 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_auto_20210606_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lga',
            name='country',
        ),
        migrations.RemoveField(
            model_name='lga',
            name='state',
        ),
    ]
