Projeto Django

1- Criar projeto Django no pycharm, com admin habilitado e app name definido

2- Criar conexão db: postgres

3- Instalar dependências
$ python.exe -m pip install --upgrade pip
$ pip install psycopg2-binary djangorestframework django-filter
$ pip freeze > requirements.txt

4- Configurar settings.py
INSTALLED_APPS = [
    'rest_framework',
    'django_filters'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oficina',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }
}

5- Editar arquivo models.py (dentro da pasta do app)
from django.db import models

class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True
    )
    created_at = models.DateTimeField(
        db_column='dt_created',
        auto_now_add=True,
        null=True
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified',
        auto_now=True,
        null=True
    )
    active = models.BooleanField(
        db_column='cs_active',
        null=False,
        default=True
    )
    class Meta:
        abstract = True
        managed = True

class Client(ModelBase):
    name = models.CharField(
        db_column='tx_nome',
        max_length=70,
        null=False
    )
    phone = models.CharField(
        db_column='tx_fone',
        max_length=10,
        null=False
    )
    email = models.CharField(
        db_column='tx_email',
        max_length=70,
        null=False
    )
    def __str__(self):
        return f"{self.id} - {self.name}"

class Vehicle(ModelBase):
    model = models.CharField(
        db_column='tx_modelo',
        max_length=20,
        null=False
    )
    brand = models.CharField(
        db_column='tx_marca',
        max_length=20,
        null=False
    )
    year = models.IntegerField(
        db_column='nb_ano',
        null=False
    )
    def __str__(self):
        return f"{self.id} - {self.model}"

class Service(ModelBase):
    client = models.ForeignKey(
        Client,
        db_column='id_client',
        null=False,
        on_delete=models.DO_NOTHING
    )
    vehicle = models.ForeignKey(
        Vehicle,
        db_column='id_vehicle',
        null=False,
        on_delete=models.DO_NOTHING
    )
    repair = models.CharField(
        db_column='tx_reparo',
        max_length=255,
        null=False
    )
    cost = models.IntegerField(
        db_column='nb_custo',
        null=False
    )
    def __str__(self):
        return (f"Custo:{self.cost} - Reparo:{self.repair}",
                f"Cliente:{self.client}, "
                f"Vehicle:{self.vehicle.model}, "
                f"Vehicle:{self.vehicle.brand}, ")

6- Migrations
$ python manage.py showmigrations
$ python manage.py makemigrations
% python manage.py migrate

7- Criar arquivo python: app(oficina) > serializers.py
from rest_framework import serializers
from oficina.models import Client,Vehicle,Service

class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=3,
        max_length=20,
        error_messages={
            'max_length': 'O nome deve ter no máximo 20 caracteres.',
            'min_length': 'O nome deve ter no mínimo 3 caracteres.'
        }
    )
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email']

class VehicleSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(
        min_value=2015,
        error_messages={
            'min_value': 'Veículo muito velho! (mín: 2015~).'
        }
    )
    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'brand', 'year']

class ServiceSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), source='vehicle', write_only=True)
    class Meta:
        model = Service
        fields = ['id', 'client_id', 'client', 'vehicle_id', 'vehicle', 'repair', 'cost']

8- Configurar: app(oficina) > views.py
from rest_framework import viewsets, permissions
from oficina.models import Client, Vehicle, Service
from oficina.serializers import ClientSerializer, VehicleSerializer, ServiceSerializer
from oficina.filters import ClientFilter, VehicleFilter, ServiceFilter
from django_filters.rest_framework import DjangoFilterBackend

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = VehicleFilter

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

9- Criar python: app(oficina) > urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from oficina.views import ClientViewSet, VehicleViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'vehicle', VehicleViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

10- Editar: projetao > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('oficina.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

11- Adicionar no projetao>settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework.DjangoFilterBackend'
}

12- Criar filtros: app(oficina) > filters.py
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

13- Criar superadmin
$ python manage.py createsuperuser

14- Configurar app para rodar como localhost
$ python manage.py runserver

15 - Run

16 - Testar get/post, subir para github
