from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoUser


class Department(models.Model):
    name = models.CharField(max_length=10)


class User(DjangoUser):
    department = models.ForeignKey('Department', null=True)

    def group_list(self):
    	return '|'.join(self.groups.all().values_list('name', flat=True))