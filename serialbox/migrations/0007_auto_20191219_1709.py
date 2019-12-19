# Generated by Django 2.2.7 on 2019-12-19 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serialbox', '0006_auto_20190128_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='machine_name',
            field=models.CharField(help_text='A url/api-friendly unique key for use in API calls and such.', max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9\\-\\_]*$', 'Only numbers and letters are allowed. Invalid API Key.')], verbose_name='API Key'),
        ),
        migrations.AlterField(
            model_name='sequentialregion',
            name='machine_name',
            field=models.CharField(help_text='A url/api-friendly unique key for use in API calls and such.', max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9\\-\\_]*$', 'Only numbers and letters are allowed. Invalid API Key.')], verbose_name='API Key'),
        ),
        migrations.DeleteModel(
            name='RandomizedRegion',
        ),
    ]