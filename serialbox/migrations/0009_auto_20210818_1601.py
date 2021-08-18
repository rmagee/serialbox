# Generated by Django 3.1.4 on 2021-08-18 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serialbox', '0008_randomizedregion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='response',
            options={'verbose_name': 'Request and Response', 'verbose_name_plural': 'Requests and Responses'},
        ),
        migrations.AddField(
            model_name='response',
            name='response',
            field=models.TextField(blank=True, help_text='The response data', null=True, verbose_name='Response'),
        ),
        migrations.AddField(
            model_name='response',
            name='task_name',
            field=models.CharField(default='', help_text='If a response rule was configured for the pool and the request was fulfilled, a task name will be supplied.', max_length=100, verbose_name='Task Name'),
            preserve_default=False,
        )
    ]
