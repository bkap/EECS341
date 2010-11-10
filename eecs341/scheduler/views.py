import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
# Create your views here.
def login(request) :
	if request.method == 'GET' :
		c = {}
		c.update(csrf(request))
		return render_to_response('login.html',c)
	else :
		return HttpResponse("You've attempted to log in %s" %
		request.POST['uname'])
def hello(request) :
	if request.method == 'POST' :
		u = User.objects.get(username__exact=request.POST['uname'])
		if u.check_password(request.POST['pword']) :
			return render_to_response('welcome.html',{'user':u})
		else :
			return HttpResponse("Login unsuccesful. Press back and try again")
