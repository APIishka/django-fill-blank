# Generated by Django 4.2.11 on 2024-05-01 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='answer',
        ),
        migrations.AddField(
            model_name='userresponse',
            name='answer_text',
            field=models.CharField(default='', max_length=255),
        ),
    ]
