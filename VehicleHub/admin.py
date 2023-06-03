from django.contrib import admin
from .models import CustomUser, Organisation, OrganisationType, Vehicle, CustomsRecord, Ownership, NumberPlate, RegistrationRecord, FinanceRecord, BreachType, PunishmentType, PoliceRecord, AccidentRecord, PolicyRecord, MaintenanceType, MaintenanceRecord

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Organisation)
admin.site.register(OrganisationType)
admin.site.register(Vehicle)
admin.site.register(CustomsRecord)
admin.site.register(Ownership)
admin.site.register(NumberPlate)
admin.site.register(RegistrationRecord)
admin.site.register(FinanceRecord)
admin.site.register(BreachType)
admin.site.register(PunishmentType)
admin.site.register(PoliceRecord)
admin.site.register(AccidentRecord)
admin.site.register(PolicyRecord)
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceRecord)
