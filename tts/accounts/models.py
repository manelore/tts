from django.db import models
from django.contrib.auth.models import User as DjangoUser


class Department(models.Model):
    name = models.CharField(max_length=10)


class User(DjangoUser):
    department = models.ForeignKey('Department')
