from django import forms
from .models import Show, Country

class ShowForm(forms.ModelForm):
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all().order_by('country_name'),
        widget=forms.SelectMultiple(attrs={'class': 'flat-input', 'style': 'height: 150px;'}),
        label="Страны производства (зажмите Ctrl для выбора нескольких)",
        required=False
    )

    class Meta:
        model = Show
        fields = ['title', 'type', 'release_year', 'rating', 'duration', 'description']

        labels = {
            'title': 'Название',
            'type': 'Тип (Movie/TV Show)',
            'release_year': 'Год выпуска',
            'rating': 'Возрастной рейтинг',
            'duration': 'Длительность',
            'description': 'Описание',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'flat-input', 'placeholder': 'Например: Titanic'}),
            'type': forms.TextInput(attrs={'class': 'flat-input'}),
            'release_year': forms.NumberInput(attrs={'class': 'flat-input'}),
            'rating': forms.TextInput(attrs={'class': 'flat-input'}),
            'duration': forms.TextInput(attrs={'class': 'flat-input'}),
            'description': forms.Textarea(attrs={'class': 'flat-input', 'rows': 4}),
        }
