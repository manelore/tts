from django.shortcuts import render


def login(request):
	return render(request, 'accounts/login.html')


def overview(request):
	return render(request, 'accounts/overview.html')
