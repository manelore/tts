from django.db import models
from django.contrib.auth.models import User as DjangoUser


class Department(models.Model):
    name = models


class User(DjangoUser):
    department = models.ForeignKey('Department')
