# Generated by Django 3.2 on 2021-07-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='scores',
            name='approval_status',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
