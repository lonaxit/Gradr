# Generated by Django 3.2 on 2021-06-20 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20210620_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scores',
            old_name='firstscores',
            new_name='firstscore',
        ),
        migrations.RenameField(
            model_name='scores',
            old_name='secondscores',
            new_name='secondscore',
        ),
        migrations.RenameField(
            model_name='scores',
            old_name='thirdscores',
            new_name='thirdscore',
        ),
    ]
