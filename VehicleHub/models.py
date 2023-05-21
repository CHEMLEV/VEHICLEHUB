from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


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
