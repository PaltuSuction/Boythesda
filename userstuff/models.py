from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    user_profile_picture = models.ImageField(upload_to = 'profilePictures/', default='static/default/64572.png')
    user_email = models.EmailField(null = True, blank=True)
    user_rating = models.SmallIntegerField(default=0)

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()