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