# Generated by Django 3.2.7 on 2021-09-19 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path_to_file', models.TextField(default='', verbose_name='Путь к файлу')),
                ('words', models.TextField(default='', verbose_name='Уникальные слова')),
            ],
        ),
    ]
