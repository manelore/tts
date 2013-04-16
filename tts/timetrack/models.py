from __future__ import print_function, division, unicode_literals, absolute_import

from django.db import models
from django.conf import settings


USER_MODEL = settings.AUTH_USER_MODEL


class WorkType(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Work type"

    def __str__(self):
        return "Work type {0}".format(self.name)


class Project(models.Model):

    users = models.ManyToManyField(USER_MODEL)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Project"


class Task(models.Model):

    description = models.CharField(max_length=500)
    estimate = models.IntegerField()
    deadline = models.DateTimeField()
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name = "Task"


class WorkLogFieldsMixin(models.Model):

    task = models.ForeignKey(Task)
    work_type = models.ForeignKey(WorkType)
    user = models.ForeignKey(USER_MODEL)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()
    active = models.BooleanField(null=False, default=True, db_index=True)

    class Meta:
        abstract = True


class WorkLog(WorkLogFieldsMixin, models.Model):

    class Meta:
        verbose_name = "Work log"


class WorkLogHistory(WorkLogFieldsMixin, models.Model):

    parent_worklog = models.ForeignKey(WorkLog)

    class Meta:
        verbose_name = "Work log history"


class Request(models.Model):

    user = models.ForeignKey(USER_MODEL)

    class Meta:
        verbose_name = "Request"


class DayOffLog(models.Model):

    user = models.ForeignKey(USER_MODEL)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()

    class Meta:
        verbose_name = "Day off"
