# Generated by Django 3.2 on 2021-10-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0022_annualresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annualresult',
            name='status',
        ),
        migrations.AddField(
            model_name='annualresult',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]