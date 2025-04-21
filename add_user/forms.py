from django.core import validators
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model() 

class Travel_Registration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    preferred_season = forms.ChoiceField(
        choices=User.TRAVEL_SEASONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    preferred_travel_type = forms.ChoiceField(
        choices=User.TRAVEL_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'password', 'preferred_season', 'preferred_travel_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class InterestSearchForm(forms.Form):
    query = forms.CharField(label="Search Interests", max_length=255)