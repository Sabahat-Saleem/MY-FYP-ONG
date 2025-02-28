from django.core import validators
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model() 

class Hod_Registration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email', 'password']
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }
# ********************new ********************