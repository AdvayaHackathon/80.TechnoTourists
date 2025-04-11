from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import HiddenGem
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class HiddenGemForm(forms.ModelForm):
    class Meta:
        model = HiddenGem
        fields = ['place_name', 'district', 'state', 'why_hidden', 'best_time_to_visit', 'latitude', 'longitude']
        widgets = {
            'why_hidden': forms.Textarea(attrs={'rows': 3}),
        }
