# Generated by Django 4.2.1 on 2023-05-08 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0003_file_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='availableChangeDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='valueChangeDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
