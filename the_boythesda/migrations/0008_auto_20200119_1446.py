# Generated by Django 2.2.5 on 2020-01-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_boythesda', '0007_auto_20191231_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(default='Жанр не указан', max_length=100, unique=True, verbose_name='Жанр'),
        ),
    ]
