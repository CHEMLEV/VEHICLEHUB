import django_filters
from .models import Organisation
from django import forms



class OrganisationFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='title',
        label='Organisation Name',
        widget=forms.TextInput(attrs={'class': 'filter_field'})
    )

    address = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='address',
        label='Address',
        widget=forms.TextInput(attrs={'class': 'filter_field'})
    )

    class Meta:
        model = Organisation
        fields = ['title', 'address']
