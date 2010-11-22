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

def search(request) :
	return render_to_response('search_form.html',{})
def searchresults(request) :
	dept = request.GET['dept'] or None
	sem_name = request.GET['semester'] or None
	course_num = request.GET['coursenum'] or None
	professor = request.GET['professor'] or None
	order = request.GET['ratio']
	semester = Semester.objects.get(name=sem_name)
	if semester is None :
		return HttpResponse("Error: unable to find semester")
	coursenum__gt=int(course_num) if order == 'gt' else None
	coursenum__lt = int(course_num) if order=='lt' else None
	coursenum = int(course_num) if order=="eq" else None
	
	#TODO: figrue out how to do this query efficiently
	return render_to_response("search.html",{user:request.user,
	courses:Class.objects.all()})
