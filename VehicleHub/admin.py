from django.contrib import admin
from .models import CustomUser, Organisation, OrganisationType

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Organisation)
admin.site.register(OrganisationType)
