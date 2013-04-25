from django.shortcuts import render

from timetrack.models import Task


def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'timetrack/task_list.html', {'tasks': tasks})


def index(request):
    return render(request, 'layout.html')
