# Generated by Django 4.2.1 on 2023-05-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0002_rename_is_available_file_isavailable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
