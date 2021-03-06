# Generated by Django 2.2.5 on 2019-10-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstuff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_rating',
            field=models.SmallIntegerField(default=0),
        ),
    ]
