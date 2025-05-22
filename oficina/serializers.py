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