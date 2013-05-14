from datetime import datetime, timedelta
import csv

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from timetrack.models import *  # noqa
from timetrack.forms import FilterForm, RequestForm, WorkLogForm, UserWorkLogReportForm, ProjectReportForm, ExportForm
from accounts.models import User

import tempfile
import subprocess


def tasks(request):
    if not request.user.is_authenticated():
        return redirect('tts_login')
    ff = FilterForm(request.GET)

    tasks = TaskWithTime.objects.filter(project__in=request.user.project_set.all())
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


def worklog_edit(request, id=0):
    wl = get_object_or_404(WorkLog, pk=id)
    form = WorkLogForm(instance=wl)
    if request.method == "POST":
        form = WorkLogForm(instance=wl, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('worklog')
    return render(request, 'timetrack/track_time.html', {'form': form})


def generate_report(request, header, rows):

    isxls = request.POST.get('xls')

    _, filename = tempfile.mkstemp(prefix="report", suffix=".csv")
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    if isxls:
        _, new_file = tempfile.mkstemp(prefix="report", suffix=".xls'")
        subprocess.check_call(['ssconvert', '-T', 'Gnumeric_Excel:excel_dsf', filename, new_file])
        filename = new_file

    r = open(filename, 'r')

    if isxls:
        response = HttpResponse(r, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xls"'
    else:
        response = HttpResponse(r, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

    return response


def reports(request):
    print request.POST
    uw_form = UserWorkLogReportForm()
    pr_form = ProjectReportForm()
    if request.method == "POST":
        form_type = request.POST.get('csv') or request.POST.get('xls')
        if not form_type:
            return render(request, 'timetrack/reports.html', {'uw_form': uw_form})
        elif form_type == 'uw':
            uw_form = UserWorkLogReportForm(request.POST)
            if uw_form.is_valid():
                data = uw_form.cleaned_data
                header = ['start_at', 'finish_at', 'worktype', 'task', 'project']
                rows = report_select_user_worklog(data['user'], data['start_at'], data['finish_at'])
                return generate_report(request, header, rows)
        elif form_type == 'pr':
            pr_form = ProjectReportForm(request.POST)
            if pr_form.is_valid():
                header = ['Username', 'Task', 'Task_Description', 'Work_Type', 'Work_time', 'Date']
                rows = report_select_project_report(pr_form.cleaned_data['project'])
                return generate_report(request, header, rows)

    return render(request, 'timetrack/reports.html', {'uw_form': uw_form, 'pr_form': pr_form})


def import_worklogs(data):

    data = data[1:]

    worktypes = {}
    for wt in WorkType.objects.all():
        worktypes[wt.name] = wt

    toinsert = []
    for fromd, tod, tname, uname, wtname in data:
        
        if wtname not in worktypes:
            worktypes[wt.name] = wt = WorkType.objects.create(name=wtname)
        else:
            wt = worktypes[wtname]

        user = User.objects.get(username=uname)
        task = Task.objects.get(name=tname)
        fromd = datetime.strptime(fromd, "%Y-%m-%d %H:%M")
        tod = datetime.strptime(tod, "%Y-%m-%d %H:%M")

        wl = WorkLog(user=user, task=task, start_at=fromd, finish_at=tod, work_type=wt)
        toinsert.append(wl)


    WorkLog.objects.bulk_create(toinsert)
    


def export(request):
    form = ExportForm()
    is_admin = 'admin' in request.user.groups.values_list('name', flat=True)
    if request.method == "POST":
        form = ExportForm(request.POST, request.FILES)
        if form.is_valid():
            data = list(csv.reader(form.cleaned_data['exp_file']))
            # start at - end at - task - user
            print data
            import_worklogs(data)

    return render(request, 'timetrack/export.html', {'form': form, 'is_admin': is_admin})