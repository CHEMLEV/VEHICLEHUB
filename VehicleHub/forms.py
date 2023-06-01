from django import forms
from django.contrib.auth.forms import UserCreationForm
from VehicleHub.models import CustomUser
from .models import Organisation

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser 
        fields = ['first_name', 'last_name',  'email','password1', 'password2']


class OrganisationForm(forms.Form):
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())
    search = forms.CharField(max_length=100)
