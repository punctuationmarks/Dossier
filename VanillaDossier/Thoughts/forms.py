from django import forms
from django.contrib.auth.models import User
from .models import ThoughtsModel


class ThoughtsModelForm(forms.ModelForm):

    class Meta:
        model = ThoughtsModel
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'body': forms.TextInput(attrs={'placeholder': 'body'}),
        }


class ThoughtsModelUpdateForm(forms.ModelForm):
    
    class Meta:
        model = ThoughtsModel
        fields = ['title', 'body']