# Generated by Django 2.0.1 on 2018-07-25 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serialbox', '0002_randomizedregion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pool',
            options={'permissions': (('allocate_numbers', 'Can allocate numbers.'),), 'verbose_name': 'Pool', 'verbose_name_plural': 'Pools'},
        ),
    ]
