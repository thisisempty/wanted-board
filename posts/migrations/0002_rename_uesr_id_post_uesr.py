# Generated by Django 3.2.8 on 2021-10-24 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='uesr_id',
            new_name='uesr',
        ),
    ]
