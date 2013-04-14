
from django.db import models
from django.conf import settings


USER_MODEL = settings.AUTH_USER_MODEL


class WorkType(models.Model):
    name = models.CharField(max_length=50)


class Project(models.Model):
    users = models.ManyToManyField(USER_MODEL)
    name = models.CharField(max_length=100)


class Task(models.Model):
    description = models.CharField(max_length=500)
    estimate = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    project = models.ForeignKey(Project)


class WorkLogFieldsMixin(object):
    task = models.ForeignKey(Task)
    work_type = models.ForeignKey(WorkType)
    user = models.ForeignKey(USER_MODEL)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()
    active = models.BooleanField(null=False, default=True, db_index=True)


class WorkLog(models.Model, WorkLogFieldsMixin):
    pass


class WorkLogHistory(models.Model, WorkLogFieldsMixin):
    parent_worklog = models.ForeignKey(WorkLog)


class Request(models.Model):
    user = models.ForeignKey(USER_MODEL)


class DayOffLog(models.Model):
    user = models.ForeignKey(USER_MODEL)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()
