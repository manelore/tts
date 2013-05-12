from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from timetrack.models import *  # noqa
from timetrack.forms import FilterForm, RequestForm, WorkLogForm



def tasks(request):
    if not request.user.is_authenticated():
        return redirect('tts_login')
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
    if not request.user.is_authenticated():
        return redirect('tts_login')
    requests = Request.objects.filter(created_date__gt=datetime.now() - timedelta(days=1))
    return render(request, 'accounts/overview.html', {'requests': requests})


def project(request, slug=''):
    if not request.user.is_authenticated():
        return redirect('tts_login')
    try:
        pr = Project.objects.get(slug=slug)
    except Project.DoesNotExist:
        return Http404
    return render(request, 'timetrack/project.html', {'project': pr})


def ooo_request(request):
    request_list = request.user.request_set.all().order_by('-created_date')
    paginator = Paginator(request_list, 10)
    page = request.GET.get('page')
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    return render(request,
                  'timetrack/request.html', 
                  {'new_request': False, 
                   'requests': requests})


def new_request(request):
    form = RequestForm(initial={'user': request.user})
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'timetrack/request.html', {'new_request': True, 'form': form})


def track_time(request, taskid=0):    
    try:
        task = Task.objects.get(id=taskid)
        user = request.user
        form = WorkLogForm(initial={'user': user, 'task': task})
        if request.method == "POST":
            
            form = WorkLogForm(request.POST)
            if form.is_valid():
                form.save()
        return render(request, 'timetrack/track_time.html', {'form': form})
    except Task.DoesNotExist:
        raise Http404


def worklog(request):
    user = request.user
    worklog = user.worklog_set.all()
    return render(request, 'timetrack/worklog.html', {'worklog': worklog})