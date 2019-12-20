from django import forms
from django.contrib.auth.models import User

from userstuff.models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_email', 'user_profile_picture')