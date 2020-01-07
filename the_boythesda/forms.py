from django import forms

from the_boythesda.models import Genre


class SearchForm(forms.Form):
    query = forms.CharField()

class GenreChoiceForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Genre
        exclude = ['id', 'name']
