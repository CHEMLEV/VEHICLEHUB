from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .models import (
    Organisation, Vehicle, CustomsRecord, Ownership, NumberPlate, FinanceRecord, 
    PoliceRecord, AccidentRecord, MaintenanceRecord )
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

def add_record_types_view(request):
    return render(request, 'add_record_types.html')


def HomePageView(request):
    return render (request, 'home.html') 



def vehicle_filter_list(request, template_name):
    
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

    return render(request, template_name, context)

# Vehicles
class VehiclesListView(ListView):
    model = Vehicle
    template_name = "request_report.html"

    def get(self, request, *args, **kwargs):
        view = views.vehicle_filter_list
        return view(request, "request_report.html", *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = views.vehicle_filter_list
        return view(request, "request_report.html", *args, **kwargs)
    

class VehicleDetailsView(DetailView): 
    model = Vehicle
    template_name = "report_details.html"


class SearchEditListView(ListView):
    model = Vehicle
    template_name = "search_edit.html"

    def get(self, request, *args, **kwargs):
        view = views.vehicle_filter_list
        return view(request, "search_edit.html", *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = views.vehicle_filter_list
        return view(request, "search_edit.html", *args, **kwargs)
    

class SearchEditDetailsView(DetailView): 
    model = Vehicle
    template_name = "search_edit_details.html"


class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ['year', 'brand', 'model', 'fuel', 'output', 'drivetrain', 'trim_line', 'registered_owner_user_id']
    template_name = "record_edit.html"
    success_url = reverse_lazy('search_edit_details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = "vehicle"
        context['VIN'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('ui')

    def test_func(self):
        obj = self.get_object()
        return obj.developer == self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registered_owner_user_id'].required = False
        return form


class CustomsRecordUpdateView(UpdateView):  
    model = CustomsRecord
    fields = ['record_date', 'mileage', 'import_as', 'damaged', 'country_of_origin']
    template_name = "record_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = "customs"
        context['VIN'] = self.object.vehicle_id.VIN
        return context

    def get_success_url(self):
        return reverse_lazy('ui')

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user
    
    
class OwnershipUpdateView(UpdateView):  
    model = Ownership
    fields = ['record_date', 'mileage', 'new_owner']
    template_name = "record_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = "ownership"
        context['VIN'] = self.object.vehicle_id.VIN
        return context
    def get_success_url(self):
        return reverse_lazy('ui')

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user 


class NumberPlateUpdateView(UpdateView):  
    model = NumberPlate
    fields = ['record_date', 'mileage', 'new_plates']
    template_name = "record_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = "number plates"
        context['VIN'] = self.object.vehicle_id.VIN
        return context
    def get_success_url(self):
        return reverse_lazy('ui')

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user 
 

class FinanceRecordUpdateView(UpdateView):  
    model = FinanceRecord
    fields = ['record_date', 'mileage', 'expiry_date', 'actual_completion_date']
    template_name = "record_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = "finance"
        context['VIN'] = self.object.vehicle_id.VIN
        return context
    def get_success_url(self):
        return reverse_lazy('ui')

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user 


class AccidentRecordUpdateView(UpdateView):  
    model = AccidentRecord
    fields = '__all__'
    template_name = "record_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = self.kwargs.get('plate') + ' AccidentRecord'
        return context

    def get_success_url(self):
        return reverse_lazy('search_edit_details', kwargs={'pk': self.kwargs.get('vehicle_pk')})

    def test_func(self):  # new
        obj = self.get_object()
        return obj.developer == self.request.user


class PoliceRecordUpdateView(UpdateView):  
    model = PoliceRecord
    fields = '__all__'
    template_name = "record_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = self.kwargs.get('plate') + ' PoliceRecord'
        return context

    def get_success_url(self):
        return reverse_lazy('search_edit_details', kwargs={'pk': self.kwargs.get('vehicle_pk')})

    def test_func(self):  # new
        obj = self.get_object()
        return obj.developer == self.request.user


class MaintenanceRecordUpdateView(UpdateView):  
    model = MaintenanceRecord
    fields = '__all__'
    template_name = "record_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = self.kwargs.get('plate') + ' MaintenanceRecord'
        return context

    def get_success_url(self):
        return reverse_lazy('search_edit_details', kwargs={'pk': self.kwargs.get('vehicle_pk')})

    def test_func(self):  # new
        obj = self.get_object()
        return obj.developer == self.request.user


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    template_name = "record_new.html"
    fields = '__all__'
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'vehicle'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registered_owner_user_id'].required = False 
        return form


class CustomsRecordCreateView(LoginRequiredMixin, CreateView):
    model = CustomsRecord
    template_name = "record_new.html"
    fields = ["vehicle_id", "record_date", "import_as", "damaged", "mileage", "country_of_origin"]  
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'customs'
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class OwnershipCreateView(LoginRequiredMixin, CreateView):  # new 
    model = Ownership
    template_name = "record_new.html"
    fields = '__all__'
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'ownership'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('user_id')
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class NumberPlateCreateView(LoginRequiredMixin, CreateView):  # new 
    model = NumberPlate
    template_name = "record_new.html"
    fields = '__all__'
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'number plates'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('user_id')
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class FinanceRecordCreateView(LoginRequiredMixin, CreateView):  # new 
    model = FinanceRecord
    template_name = "record_new.html"
    fields = '__all__'
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'finance'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('user_id')
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class AccidentRecordCreateView(LoginRequiredMixin, CreateView):  # new 
    model = AccidentRecord
    template_name = "record_new.html"
    fields = '__all__'
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'accident'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('user_id')
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class PoliceRecordCreateView(LoginRequiredMixin, CreateView): 
    model = PoliceRecord
    template_name = "record_new.html"
    fields = ["vehicle_id", "record_date", "breach_type_id", "punishment_type_id", "due_date", "expiry_date", "comment"]  
    success_url = reverse_lazy('add_record_types')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'offence'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['expiry_date'].required = False 
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class MaintenanceRecordCreateView(LoginRequiredMixin, CreateView):  # new 
    model = MaintenanceRecord
    template_name = "record_new.html"
    fields = '__all__'
    success_url = reverse_lazy('add_record_types')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_model'] = 'maintenance'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('user_id')
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class VehicleDeleteView(DeleteView): #LoginRequiredMixin, UserPassesTestMixin, 
    model = Vehicle
    fields = (
        "VIN",
        "year",
    )
    template_name = "vehicle_delete.html"
    success_url = reverse_lazy('manage_records')

    def test_func(self):  # new
        obj = self.get_object()
        return obj.developer == self.request.user
