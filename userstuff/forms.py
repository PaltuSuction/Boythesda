from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from userstuff.models import UserProfile


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')

    def _post_clean(self):
        super()._post_clean()
        cd = self.cleaned_data
        try:
            password = cd['password1']
            if password:
                try:
                    password_validation.validate_password(password, self.instance)
                except forms.ValidationError as error:
                    self.add_error('password2', error)
        except:
            pass


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_email', 'user_profile_picture')

        widgets = {
            'user_email' : forms.EmailInput
        }

