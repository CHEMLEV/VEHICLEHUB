from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import RegisterForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Organisation
import django_filters




class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect(reverse('join'))
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('join'))
        else:
            # Invalid credentials, handle the error as needed
            error_message = 'Invalid email or password.'
            return render(request, 'registration/login.html', {'error_message': error_message})
    
    return render(request, 'registration/login.html')



def join_view(request):
    organisations = Organisation.objects.all()
    context = {'organisations': organisations}
    return render(request, 'join.html', context)

