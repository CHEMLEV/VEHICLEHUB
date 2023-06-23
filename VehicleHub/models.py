from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime    


class OrganisationType(models.Model):
    organisation_type = models.TextField(max_length=100, null=False)

    def __str__(self):
        return self.organisation_type


class Organisation(models.Model):
    title = models.TextField(max_length=100, null=False)
    address = models.TextField(max_length=200, null=False)
    phone = models.IntegerField(null=False)
    organisation_type = models.ForeignKey(OrganisationType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.email
    

class VehicleMake(models.Model):
    brand = models.TextField(max_length=30, null=False)
    logo_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.brand


class Vehicle(models.Model):
    VIN = models.TextField(max_length=20, null=False)
    year = models.IntegerField(null=False)
    brand = models.ForeignKey(VehicleMake, on_delete=models.CASCADE)
    model = models.TextField(max_length=20, null=False)
    fuel = models.TextField(max_length=20, null=False)
    output = models.IntegerField(null=False)
    drivetrain = models.TextField(max_length=20, null=False)
    trim_line = models.TextField(max_length=20, null=False)
    registered_owner_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.VIN


class CustomsRecord(models.Model):
    
    vehicle_id = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    record_date = models.DateField(default=datetime.now, null=False)
    import_as = models.TextField(max_length=4, default="")
    damaged = models.TextField(max_length=3, default="")
    mileage = models.IntegerField(null=False)
    country_of_origin = models.TextField(max_length=30, null=False)

    def __str__(self):
        return str(self.id)


class Ownership(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    record_date = models.DateField(default=datetime.now, null=False)
    mileage = models.IntegerField(null=False)
    new_owner = models.TextField(max_length=50, null=False)

    def __str__(self):
        return str(self.id)


class NumberPlate(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    record_date = models.DateField(default=datetime.now, null=False)
    mileage = models.IntegerField(null=False)
    new_plates = models.TextField(max_length=30, null=False)

    def __str__(self):
        return str(self.new_plates)



class FinanceRecord(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    record_date = models.DateField(default=datetime.now, null=False)
    mileage = models.IntegerField(null=False)
    expiry_date = models.DateField(default=datetime.now, null=False)
    actual_completion_date = models.DateField(null=True)
    
    def __str__(self):
        return str(self.id)


class BreachType(models.Model):
    breach_type_title = models.TextField(max_length=500, null=False)

    def __str__(self):
        return self.breach_type_title

class PunishmentType(models.Model):
    punishment_type_title = models.TextField(max_length=500, null=False)

    def __str__(self):
        return self.punishment_type_title


class PoliceRecord(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    record_date = models.DateField(default=datetime.now, null=False)
    breach_type_id = models.ForeignKey(BreachType, on_delete=models.CASCADE, null=True)
    punishment_type_id = models.ForeignKey(PunishmentType, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(default=datetime.now, null=False)
    expiry_date = models.DateField(default=datetime.now, null=True)
    comment = models.TextField(max_length=300, blank=True)
    
    def __str__(self):
        return str(self.id)


class AccidentRecord(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    record_date = models.DateField(default=datetime.now, null=False)
    mileage = models.IntegerField(null=False)
    other_participants = models.TextField(max_length=80, null=True)
    comment = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.id

class MaintenanceType(models.Model):
    maintenance_type_title = models.TextField(max_length=500, null=False)

    def __str__(self):
        return self.maintenance_type_title


class MaintenanceRecord(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    maintenance_type_id = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, null=True)
    record_date = models.DateField(default=datetime.now, null=False)
    mileage = models.IntegerField(null=False)
    comment = models.TextField(max_length=500)
    products_used = models.TextField(max_length=500)
   

    def __str__(self):
        return self.id


