from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .models import Organisation
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



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
    context = {
        'organisations': organisations,
    }

    if request.method == 'POST':
        organisation_id = request.POST.get('organisation_id')
        if organisation_id:
            organisation = Organisation.objects.get(id=organisation_id)
            request.user.organisation_id = organisation.id
            request.user.save()
            return JsonResponse({'success': True})

    return render(request, 'join.html', context)





def request_sent_view(request):
    return render(request, 'request_sent.html')
