# Generated by Django 2.2.5 on 2020-01-12 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstuff', '0003_auto_20200109_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_picture',
            field=models.ImageField(upload_to='profilePictures/'),
        ),
    ]
