# Generated by Django 3.2 on 2021-08-25 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0016_subject_subject_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_code',
            field=models.CharField(default='CMP', max_length=6),
        ),
    ]
