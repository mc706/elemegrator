from django import forms
from .models import Feed, Category


class CateogryForm(forms.ModelForm):
    """Form for creating a new category"""
    
    class Meta:
        model = Category
        fields = ('name')


class FeedForm(forms.ModelForm):
    """Form for creating a new feed"""
    
    class Meta:
        model = Feed
        exclude = (
            'elements',
            'published',
        )
        
