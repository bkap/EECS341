import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from scheduler.models import *
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

def search_form(request) :
	return render_to_response('searchform.html',{'semesters':Semester.objects.all()})
def searchresults(request) :
	queries = {}
	dept = request.GET['dept']
	if dept :
		queries['course__dept'] = dept
	sem_name = request.GET['semester']
	if sem_name :
			queries['semester__name'] = sem_name
	course_num = request.GET['coursenum']
	professor = request.GET['professor']
	if professor:
		queries['professor'] = professor
	order = request.GET['ratio']
	if order == 'eq' :
		queries['course__number'] = coursenum
	else :
		queries['course__number__%s' % order] = coursenum
	return render_to_response("search.html",{user:request.user,
	courses:Class.objects.filter(**queries)})
