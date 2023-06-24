import django_filters
from .models import Organisation, Vehicle, NumberPlate, CustomsRecord
from django import forms
from django.db.models import Subquery, OuterRef



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


class VehicleFilter(django_filters.FilterSet):
    vin = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='VIN',
        label='VIN     ',
        widget=forms.TextInput(attrs={'class': 'filter_field'})
    )

    numberplates = django_filters.CharFilter(
        lookup_expr='icontains',
        method='filter_numberplates',
        label='PLATES',
        widget=forms.TextInput(attrs={'class': 'filter_field'})
    )

    def filter_numberplates(self, queryset, name, value):
        latest_numberplate_ids = NumberPlate.objects.filter(
            vehicle_id=OuterRef('pk')
        ).order_by('-record_date').values('id')[:1]

        return queryset.filter(
            numberplate__id__in=Subquery(latest_numberplate_ids),
            numberplate__new_plates__icontains=value
        )

    class Meta:
        model = Vehicle
        fields = ['numberplates', 'vin']


from django import template

register = template.Library()

@register.filter
def break_loop(value, condition):
    for item in value:
        if condition(item):
            break
    return item