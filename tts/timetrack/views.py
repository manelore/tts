from django.shortcuts import render
from django import forms

from timetrack.models import *  # noqa


class FilterForm(forms.Form):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    project = forms.ModelChoiceField(
       required=False,
       queryset=Project.objects.all() if Project.objects.all().count() > 0 else Project.objects.get_empty_query_set(),
       empty_label="Any project",
    )
    min_estimate = forms.IntegerField(min_value=0, required=False)
    max_estimate = forms.IntegerField(min_value=0, max_value=99999, required=False)


def tasks(request):

    ff = FilterForm(request.GET)

    tasks = TaskWithTime.objects.all()
    if ff.is_valid():

        start_date = ff.cleaned_data['start_date']
        end_date = ff.cleaned_data['end_date']
        project = ff.cleaned_data['project']
        min_estimate = ff.cleaned_data['min_estimate']
        max_estimate = ff.cleaned_data['max_estimate']

        if start_date:
            tasks = tasks.filter(deadline__gte=start_date)
        if end_date:
            tasks = tasks.filter(deadline__lte=end_date)
        if project:
            tasks = tasks.filter(project=project)
        if min_estimate:
            tasks = tasks.filter(estimate__gte=min_estimate)
        if max_estimate:
            tasks = tasks.filter(estimate__lte=max_estimate)

    return render(
        request,
        'timetrack/task_list.html',
        {'tasks': tasks, 'fform': ff},
    )


def index(request):
	requests = Request.objects.all()
	return render(request, 'accounts/overview.html', {'requests': requests})


def project(request, slug=''):
	return render(request, 'layout.html')
