from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from accounts.models import User


def signin(request):
	if request.user.is_authenticated():
		return redirect('index')
	error = ''
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		print username, password
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			error = 'Invalid username/password combination'
	return render(request, 'accounts/login.html', {'login_error': error})


@login_required
def common(request):
	users_list = User.objects.all()
	paginator = Paginator(users_list, 2) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return render(request, 'accounts/common.html', {'profiles': users})


def profile(request, id=0):
	try:
		user = User.objects.get(id=id)
		return render(request, 'accounts/profile.html', {'profile': user})
	except User.DoesNotExist:
		raise Http404
