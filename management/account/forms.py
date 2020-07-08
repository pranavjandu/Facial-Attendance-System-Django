from django.forms import ModelForm
from .models import Students
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class StudentForm(ModelForm):
    class Meta:
        model = Students
        fields = ['name','batch_id']

class CreateUserModel(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']