# Generated by Django 3.2.9 on 2021-11-05 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfiles',
            name='size',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
