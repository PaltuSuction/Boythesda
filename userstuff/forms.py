from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from userstuff.models import UserProfile


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_email', 'user_profile_picture')

        widgets = {
            'user_email' : forms.EmailInput
        }

