
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
 
 
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    college = forms.CharField(max_length=200, required=False)
    branch = forms.CharField(max_length=200, required=False)
    year = forms.CharField(max_length=10, required=False)
 
    class Meta:
        model = User
        fields = ['username', 'email', 'college', 'branch', 'year', 'password1', 'password2']
 
 
class LoginForm(AuthenticationForm):
    pass
 
 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_pic', 'skills', 'college', 'branch', 'year', 'github', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
 