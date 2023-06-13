from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .models import Organisation, Vehicle
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from . import views
from .filters import VehicleFilter



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


def ui_view(request):
    return render(request, 'ui.html')

def manage_records_view(request):
    return render(request, 'manage_records.html')


def HomePageView(request):
    return render (request, 'home.html') 



def vehicle_filter_list(request):
    
    vehicles = Vehicle.objects.all()

    vehicleFilter = VehicleFilter(queryset=vehicles)

    if request.method == "POST":
        vehicleFilter = VehicleFilter(request.POST, queryset=vehicles)

    for vehicle in vehicleFilter.qs:
    
        numberplates_list = list(vehicle.numberplate_set.all().values_list('new_plates', flat=True))
        vehicle.numberplates = numberplates_list[-1] if numberplates_list else ""


    context = {
        'vehicleFilter': vehicleFilter
    }

    return render(request, 'request_report.html', context)

# Vehicles
class VehiclesListView(ListView):
    model = Vehicle
    template_name = "request_report.html"

    def get(self, request, *args, **kwargs):
        view = views.vehicle_filter_list
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = views.vehicle_filter_list
        return view(request, *args, **kwargs)
    

class VehicleDetailsView(DetailView): 
    model = Vehicle
    template_name = "report_details.html"


class VehicleCreateView(LoginRequiredMixin, CreateView):  # new 
    model = Vehicle
    template_name = "vehicle_new.html"
    fields = ("VIN", "year", "make", "model", "fuel", "output", "drivetrain", "trim_line")
    success_url = reverse_lazy('report')


class VehicleUpdateView(UpdateView): #LoginRequiredMixin, UserPassesTestMixin, 
    model = Vehicle
    fields = (
        "VIN", "year", "make", "model", "fuel", "output", "drivetrain", "trim_line"
    )
    template_name = "vehicle_edit.html"
    success_url = reverse_lazy('report')

    def test_func(self):  # new
        obj = self.get_object()
        return obj.developer == self.request.user


class VehicleDeleteView(DeleteView): #LoginRequiredMixin, UserPassesTestMixin, 
    model = Vehicle
    fields = (
        "VIN",
        "year",
    )
    template_name = "vehicle_delete.html"
    success_url = reverse_lazy('report')

    def test_func(self):  # new
        obj = self.get_object()
        return obj.developer == self.request.user
