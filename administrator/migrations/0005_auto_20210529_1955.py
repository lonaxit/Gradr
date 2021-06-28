# Generated by Django 3.2 on 2021-05-29 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_attendancesetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=200, null=True),
        ),
    ]