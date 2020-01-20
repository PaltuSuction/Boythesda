from django import forms
from django.contrib.auth.models import User
from django.forms import DateField

from boythesda import settings
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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser')
        exclude = ['password']

'''
class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'summary', 'genre', 'price', 'scoreCritics', 'scoreUsers', 'publisher', 'Image',
                  'releaseDate','sysReq']
        widgets = {'releaseDate': DateField(input_formats=settings.DATE_INPUT_FORMATS)}
'''


