from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
# import from app
from todoapp.models import Todos

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"enter username"}))
    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"password","type":"password"}))


class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["name"]
        
