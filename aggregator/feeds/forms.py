from django import forms
from .models import Feed, Category


class CateogryForm(forms.ModelForm):
    """Form for creating a new category"""
    
    class Meta:
        model = Category


class FeedForm(forms.ModelForm):
    """Form for creating a new feed"""
    
    class Meta:
        model = Feed
        exclude = (
            'elements',
            'published',
        )

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['type'] = "url"
