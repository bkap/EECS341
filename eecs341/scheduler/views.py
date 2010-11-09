import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
# Create your views here.
def login(request) :
	if request.method == 'GET' :
		c = {}
		c.update(csrf(request))
		return render_to_response('login.html',c)
	else :
		return HttpResponse("You've attempted to log in %s" %
		request.POST['uname'])
