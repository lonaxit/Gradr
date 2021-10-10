# Generated by Django 3.2 on 2021-10-05 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_teacher_user'),
        ('administrator', '0018_alter_subject_subject_code'),
        ('teacher', '0021_classroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annualtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('annualaverage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('annualposition', models.IntegerField(null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.client')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.student')),
                ('studentclass', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.studentclass')),
            ],
        ),
    ]