from django import forms
from django.contrib.auth.models import User

from the_boythesda.models import Genre, Game
from userstuff.forms import UserForm
from userstuff.models import UserProfile


class SearchForm(forms.Form):
    query = forms.CharField()

class GenreChoiceForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(),
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'})
                                            )
    class Meta:
        model = Genre
        exclude = ['id', 'name']

class UserUpdateForm(UserForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser')


