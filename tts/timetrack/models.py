from __future__ import print_function, division, unicode_literals, absolute_import

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from accounts.middleware import get_current_user

USER_MODEL = settings.AUTH_USER_MODEL


class WorkType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Work type"

    def __str__(self):
        return "Work type {0}".format(self.name)


class ProjectManager(models.Manager):

    def get_query_set(self):
        user = get_current_user()
        if not user:
            return super(ProjectManager, self).get_empty_query_set()
        elif user.groups.filter(name="moderator").count() > 0:
            return super(ProjectManager, self).get_query_set()
        return super(ProjectManager, self).get_query_set().filter(users__in=[user])



class Project(models.Model):

    users = models.ManyToManyField(USER_MODEL, through='UserProject')
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()

    objects = ProjectManager()
    default_manager = objects

    class Meta:
        verbose_name = "Project"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project', args=[self.slug])


class UserProject(models.Model):

    user = models.ForeignKey(USER_MODEL)
    project = models.ForeignKey(Project)
    PROJECT_ROLES = [(0, 'manager'), (1, 'user')]
    role = models.IntegerField(choices=PROJECT_ROLES, default=1)


class BaseTask(models.Model):

    description = models.CharField(max_length=500)
    estimate = models.IntegerField()
    deadline = models.DateTimeField()
    project = models.ForeignKey(Project)

    class Meta:
        abstract = True
        verbose_name = "Task"

    def __unicode__(self):
        return self.description


class Task(BaseTask):
    pass


class ReadOnlyManager(models.Manager):

    def delete(self, *args, **kwgs):
        pass


class TaskWithTime(BaseTask):

    objects = ReadOnlyManager()

    worktime = models.IntegerField()

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    class Meta:
        verbose_name = "Task"
        managed = False
        db_table = 'timetrack_task_with_time'


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
    description = models.TextField()
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    REQUEST_TYPES = [("ts", "Time shift"), ("vac", "Vacation"), ("unp", "Unpaid")]
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)

    approved_by = models.ForeignKey(USER_MODEL, related_name='approver', blank=True, null=True)

    class Meta:
        verbose_name = "Request"


class DayOffLog(models.Model):

    user = models.ForeignKey(USER_MODEL)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()

    class Meta:
        verbose_name = "Day off"
