# Generated by Django 3.2 on 2021-07-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_scores_approval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='approval_status',
            field=models.CharField(default='No', max_length=10, null=True),
        ),
    ]