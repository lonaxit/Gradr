# Generated by Django 3.2 on 2021-08-22 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0011_remove_classteacher_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectteacher',
            name='session',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.session'),
        ),
        migrations.AddField(
            model_name='subjectteacher',
            name='term',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.term'),
        ),
    ]