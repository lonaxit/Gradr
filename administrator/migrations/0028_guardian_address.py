# Generated by Django 3.2 on 2021-11-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0027_guardian'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
