from django import forms
from .models import Feed, Category, Subscription


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

class SubscriptionForm(forms.ModelForm):
    """Form for managing user"""

    class Meta:
        model = Subscription

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget - forms.HiddenInput()


