# Generated by Django 3.2 on 2021-10-21 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0019_auto_20211021_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjectteacher',
            old_name='user',
            new_name='created_by',
        ),
    ]
