# Generated by Django 3.2.16 on 2023-01-18 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='posts', to='app.Category'),
        ),
    ]
