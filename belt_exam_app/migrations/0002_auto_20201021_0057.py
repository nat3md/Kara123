# Generated by Django 2.2.4 on 2020-10-21 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
    ]
