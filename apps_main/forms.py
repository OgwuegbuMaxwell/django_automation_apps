from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Used for customizing the form fields
from django import forms



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    
    class Meta:
        model = User
        fields = ('username','email',  'password1', 'password2')


















