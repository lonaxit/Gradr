# Generated by Django 3.2 on 2021-08-09 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210619_0955'),
        ('administrator', '0011_remove_classteacher_name'),
        ('teacher', '0008_remove_result_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Psychomotor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('scores', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Studentpsychomotor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('classteacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.classteacher')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.client')),
                ('pyschomotor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.psychomotor')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.rating')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.student')),
                ('studentclass', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.studentclass')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.term')),
            ],
        ),
        migrations.CreateModel(
            name='Studentaffective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('affective', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.affective')),
                ('classteacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.classteacher')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.client')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teacher.rating')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.student')),
                ('studentclass', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.studentclass')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.term')),
            ],
        ),
    ]
