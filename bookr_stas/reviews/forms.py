from django import forms
from .models import Publisher, Review, Book
from django.contrib import auth

CHOICES = (
    ('title', 'Title'),
    ('contributor', 'Contributor')
)


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('cover', 'sample')

    cover = forms.ImageField(required=False)


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(choices=CHOICES)


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('date_edited', 'book')
        rating = forms.IntegerField(min_value=0, max_value=5)
