# Generated by Django 2.2.5 on 2019-12-30 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_boythesda', '0005_auto_20191228_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.FloatField(blank=True, default=0.0, help_text='Цена игры', max_length=9999.0, null=True, verbose_name='Цена'),
        ),
    ]
