# Generated by Django 3.2 on 2021-08-22 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0012_auto_20210822_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectteacher',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.session'),
        ),
        migrations.AlterField(
            model_name='subjectteacher',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.term'),
        ),
    ]