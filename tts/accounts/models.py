from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoUser
from django.core.urlresolvers import reverse


class Department(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField(blank=True)


class Photo(models.Model):
	image = models.ImageField(upload_to="images")


class User(DjangoUser):
    department = models.ForeignKey('Department', null=True)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    skype = models.CharField(max_length=100, blank=True)
    photo = models.ForeignKey(Photo, blank=True, null=True)

    def group_list(self):
    	return '|'.join(self.groups.all().values_list('name', flat=True))

    def get_absolute_url(self):
        return reverse('profile', args=[self.id])