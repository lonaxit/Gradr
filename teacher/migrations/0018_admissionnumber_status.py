# Generated by Django 3.2 on 2021-09-01 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0017_admissionnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionnumber',
            name='status',
            field=models.CharField(default='No', max_length=20),
        ),
    ]
