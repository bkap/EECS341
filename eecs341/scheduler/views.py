import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.
def login_page(request) :
	if request.method == 'GET' :
		c = {}
		c.update(csrf(request))
		return render_to_response('login.html',c)
	else :
		return HttpResponse("You've attempted to log in %s" %
		request.POST['uname'])
def hello(request) :
	if request.method == 'POST' :
		user = authenticate(username=request.POST['uname'], password=request.POST['pword'])
		if user is not None and user.is_active :
			login(request, user)
			return render_to_response('welcome.html',{'user':user})
		else :
			return HttpResponse("Login unsuccesful. Press back and try again")
	else :
		
		if request.user.is_authenticated() :
			return render_to_response('welcome.html',{'user':request.user})
		else :
			return HttpResponse("Please Login")	
