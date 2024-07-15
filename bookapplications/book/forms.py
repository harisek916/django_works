from django import forms
from book.models import Books
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"enter name of the book"}),
            "author":forms.TextInput(attrs={"class":"form-control","placeholder":"enter author name"}),
            "price":forms.NumberInput(attrs={"class":"form-control","placeholder":"enter price"}),
            "publisher":forms.TextInput(attrs={"class":"form-control","placeholder":"enter the name of publisher"}),
            "genre":forms.TextInput(attrs={"class":"form-control","placeholder":"enter genre"}),
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"enter username"}))
    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"enter password","type":"password"}))
