from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.contrib.auth import login
from .forms import RegisterForm


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('join')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def main_view(request):
    return render(request, 'join.html')