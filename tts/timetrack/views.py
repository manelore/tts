from django.shortcuts import render
from django.core import forms

from timetrack.models import TaskWithTime


class FilterForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    ch_deadline = forms.DateTimeField()
    ch_project = forms.CharField()


def tasks(request):

    ff = FilterForm(request.GET)
    if not ff.is_vaild():
        return "Invalid form"

    tasks = TaskWithTime.objects.all()

    return render(
        request,
        'timetrack/task_list.html',
        {'tasks': tasks})


def index(request):
    return render(request, 'layout.html')
