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
