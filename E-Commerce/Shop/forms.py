from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from . models import Customar


# User Registration
class CustomarRegistration(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {
            'email':'Email'
            }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'})
        }
        
# Customar Profile Information Form
class CustomarProfile(forms.ModelForm):
    class Meta:
        model = Customar
        fields = ['id','name','division','district','thana','villageORroad','zipcode']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control'}),
            'district':forms.TextInput(attrs={'class':'form-control'}),
            'thana':forms.TextInput(attrs={'class':'form-control'}),
            'villageORroad':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }
        

# User Login
class Login(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'auto-focus':True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current_password', 'class':'form-control'}))
    

# Password Change Form
class PasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label=_('new password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control','autofocus':True}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('confirm password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control','autofocus':True}))
    


# Password Reset Form
class PasswordReset(PasswordResetForm):
    email = forms.EmailField(label=_('Email'),max_length=50, widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
    
    
# Pass Reset Change Form
class PasswordResetForm(PasswordResetForm):
    new_password1 = forms.CharField(label=_('New password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html()) 
    new_password2 = forms.CharField(label=_('Confirm new password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))