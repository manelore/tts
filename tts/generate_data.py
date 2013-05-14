#!python

from timetrack.models import *
from accounts.models import *

import django.db.transaction
import django.db.utils

import random
import datetime
from random import choice, randint


def random_hex(f, t):
    m = (f + t + 0.5) / 2
    e = m - f
    x = -1
    while not f <= x <= t:
        x = int(random.normalvariate(m, e))
    return format(random.getrandbits(4 * x), 'x')


NUM_DEPARTMENTS = 5
NUM_USERS = 50
NUM_TASKS = 800
NUM_WORKLOGS = 5000
NUM_PROJECTS = 20
NUM_REQUESTS = 100


def memoize_list(f):
    def wrapper():
        if not hasattr(f, '_res'):
            f._res = list(f())
        return f._res
    return wrapper


@memoize_list
def departments():
    for i in range(NUM_DEPARTMENTS):
        depid = "dep_" + str(i)
        try:
            yield Department.objects.get(name=depid)
            continue
        except:
            pass
        m = Department()
        m.name = depid
        m.save()
        yield m


@memoize_list
def users():
    for i in range(NUM_USERS):
        try:
            yield User.objects.get(username=("user_" + str(i)))
            continue
        except User.DoesNotExist:
            pass

        m = User()
        m.username = "user_" + str(i)
        m.department = choice(departments())
        m.position = choice(["dev", "admin", "developer", "cleaner", "qa", "hunter", "hr"])
        m.first_name = "first-name-" + random_hex(5, 10)
        m.last_name = "last-name-" + random_hex(5, 10)
        m.save()
        yield m


@memoize_list
def worktypes():
    for i in ["programming", "dev", "testing", "blabla", "managing", "do nothing", "simulating work"]:
        wt, _ = WorkType.objects.get_or_create(name=i)
        yield wt


@memoize_list
def projects():
    for i in range(NUM_PROJECTS):
        try:
            yield Project.objects.get(slug=("project-" + str(i)))
            continue
        except Project.DoesNotExist:
            pass

        m = Project()
        m.name = "Project N" + str(i)
        m.description = "project description"
        m.slug = "project-" + str(i)
        m.save()
        yield m


@memoize_list
def tasks():
    for i in range(NUM_TASKS):
        taskid = "task_" + random_hex(5, 10)
        try:
            yield Task.objects.get(name=taskid)
            continue
        except:
            pass
        m = Task()
        m.name = taskid
        m.description = "Task description " + random_hex(5, 20)
        m.estimate = randint(2, 50)
        m.deadline = datetime.datetime.now() + datetime.timedelta(days=random.randint(-60, 30))
        m.project = choice(projects())
        m.save()
        yield m


@memoize_list
def worklogs():
    for i in range(NUM_WORKLOGS):
        m = WorkLog()
        m.user = choice(users())
        m.task = choice(tasks())
        m.start_at = datetime.datetime.now() + datetime.timedelta(days=random.randint(-60, -3))
        m.start_at += datetime.timedelta(hours=random.randint(0, 24))
        m.finish_at = m.start_at + datetime.timedelta(hours=random.randint(1, 7))
        m.work_type = choice(worktypes())
        if m.start_at.month != m.finish_at.month:
            continue
        m.save()
        yield m


@memoize_list
def user_prjects():
    u = users()
    p = projects()

    for i in range((len(u) + len(p)) * 2):
        m = UserProject()
        m.user = choice(u)
        m.project = choice(p)
        m.role = choice([0, 1])
        m.save()
        yield m


@memoize_list
def requests():
    for i in range(NUM_REQUESTS):
        m = Request()
        m.user = choice(users())
        m.description = "Description here"
        m.request_type = choice(['ts', 'vac', 'unp'])
        m.start_at = datetime.datetime.now() + datetime.timedelta(days=random.randint(-50, 30))
        m.finish_at = m.start_at + datetime.timedelta(days=random.randint(1, 14))
        m.save()
        yield m


def main():
    users()
    departments()
    tasks()
    projects()
    user_prjects()
    tasks()
    worklogs()
    requests()


if __name__ == '__main__':
    main()
