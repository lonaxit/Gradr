# Generated by Django 3.2 on 2021-10-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0024_result_date_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='scores',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
