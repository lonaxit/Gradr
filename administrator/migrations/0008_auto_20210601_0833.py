# Generated by Django 3.2 on 2021-06-01 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_resumptionsetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumptionsetting',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='resumptionsetting',
            name='term_begins',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resumptionsetting',
            name='term_ends',
            field=models.DateField(blank=True, null=True),
        ),
    ]
