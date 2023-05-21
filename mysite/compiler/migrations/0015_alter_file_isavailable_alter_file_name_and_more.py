# Generated by Django 4.2.1 on 2023-05-09 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0014_alter_file_name_alter_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='isAvailable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='compiler.user'),
        ),
        migrations.AlterField(
            model_name='file',
            name='upload',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='folder',
            name='isAvailable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='compiler.user'),
        ),
    ]
