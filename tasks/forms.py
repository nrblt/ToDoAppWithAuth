from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        # fields="__all__"
        fields=['title','complete']




# from .models import Order

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
