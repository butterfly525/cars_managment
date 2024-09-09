from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Car, Comment

# Форма для автомобиля
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'description']


# Форма для комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']