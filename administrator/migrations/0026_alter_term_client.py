# Generated by Django 3.2 on 2021-10-25 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20211025_0940'),
        ('administrator', '0025_rename_created_by_term_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.client'),
        ),
    ]
