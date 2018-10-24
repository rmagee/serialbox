# Generated by Django 2.0.1 on 2018-10-15 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quartet_capture', '0002_auto_20181001_1407'),
        ('serialbox', '0003_auto_20180725_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time that this record was created', verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, help_text='The date and time that this record was modified last.', verbose_name='Last Modified')),
                ('content_type', models.CharField(choices=[('xml', 'xml'), ('json', 'json'), ('yaml', 'yaml'), ('csv', 'csv')], help_text='The content type this response rule will handle.', max_length=100, null=True, verbose_name='Content Type')),
                ('pool', models.ForeignKey(help_text='The Pool to associate this response configuration with.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='serialbox.Pool', verbose_name='Pool')),
                ('rule', models.ForeignKey(help_text='The rule to execute during response generation.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='quartet_capture.Rule')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
