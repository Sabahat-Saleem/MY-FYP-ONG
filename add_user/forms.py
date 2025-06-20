from django.core import validators
from django import forms
from django.contrib.auth import get_user_model
from .models import User
from .models import TravelSchedule, ScheduleEntry, Feedback, FeedbackReply
User = get_user_model() 

class Travel_Registration(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Confirm Password"
    )
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
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'password', 'preferred_season', 'preferred_travel_type', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            self.add_error('confirm_password', 'Password and Confirm Password do not match.')
        
        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'preferred_season', 'preferred_travel_type', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_season': forms.Select(attrs={'class': 'form-control'}),
            'preferred_travel_type': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'preferred_season', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_season': forms.Select(attrs={'class': 'form-control'}),
        }

class InterestSearchForm(forms.Form):
    query = forms.CharField(label="Search Interests", max_length=255)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'preferred_season', 'preferred_travel_type']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'preferred_season': forms.Select(attrs={'class': 'form-control'}),
            'preferred_travel_type': forms.Select(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
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
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'preferred_season', 'preferred_travel_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class TravelScheduleForm(forms.ModelForm):
    class Meta:
        model = TravelSchedule
        fields = ['title', 'start_date', 'end_date']

class ScheduleEntryForm(forms.ModelForm):
    class Meta:
        model = ScheduleEntry
        fields = ['date', 'location', 'activity', 'accommodation']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message', 'photo']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = FeedbackReply
        fields = ['name', 'message']