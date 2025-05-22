import django_filters
from oficina.models import Client, Vehicle, Service


class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='exact')
    email = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email']


class VehicleFilter(django_filters.FilterSet):
    model = django_filters.CharFilter(lookup_expr='icontains')
    brand = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Vehicle
        fields = ['model', 'brand', 'year']


class ServiceFilter(django_filters.FilterSet):
    client_id = django_filters.NumberFilter(field_name='client__id')
    client_name = django_filters.CharFilter(field_name='client__name', lookup_expr='icontains')
    vehicle_id = django_filters.NumberFilter(field_name='vehicle__id')
    vehicle_model = django_filters.CharFilter(field_name='vehicle__model', lookup_expr='icontains')
    vehicle_brand = django_filters.CharFilter(field_name='vehicle__brand', lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['id', 'client_id', 'client_name', 'vehicle_id', 'vehicle_model', 'vehicle_brand']