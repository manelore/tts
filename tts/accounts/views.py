from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def signin(request):
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
def overview(request):
	return render(request, 'accounts/overview.html')
