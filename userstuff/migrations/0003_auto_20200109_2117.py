# Generated by Django 2.2.5 on 2020-01-09 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstuff', '0002_auto_20191009_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_picture',
            field=models.ImageField(default='static/default/default_profile_pic.jpg', upload_to='profilePictures/'),
        ),
    ]
