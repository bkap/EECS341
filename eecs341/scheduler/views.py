import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from scheduler.models import *
from django.contrib.auth.decorators import permission_required
# Create your views here.
def login_page(request) :
	if request.method == 'GET' :
		c = {}
		c.update(csrf(request))
		if request.GET.get('next',None) :
			next = 'welcome.html'
		else :
			next = request.GET['next']
		c.update('next',next)
		return render_to_response('login.html',c)
	else :
		#TODO: handle redirection
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
		queries['course__number'] = course_num
	else :
		queries['course__number__%s' % order] = course_num
	return render_to_response("search.html",{'user':request.user,
	'courses':Class.objects.filter(**queries)})
@permission_required('scheduler.can_enroll',login_url='/scheduler/login.html')
def getgrades(request) :
	if request.GET.get('sem',None) != None :
		sem = Semester.objects.get(name=request.GET['sem'])
		sched = Schedule.objects.get(user=request.user, semester=sem)
		if sched :
			classes = sched.classes_enrolled.all()
		else :
			classes = []
		return render_to_response('viewgrades.html',{'user':request.user, 'classes':classes,'semester':sem})
	semesters = [schedule.semester for schedule in Schedule.objects.filter(user=request.user)]
	return render_to_response('select_semester_grades.html',{'user':request.user,'semesters':semesters})

def set_grades(request) :
	if request.GET.get('class',None) is None :
		return HttpResponse("class not found")
	klass = Class.objects.get(id=request.GET['class'])
	if klass is None :
		return HttpResponse("class not found")
	admin = Group.get(name="SchoolAdmin")
	if klass.professor == request.user or admin in request.user.groups.all() :
		enrolled = EnrolledClass.objects.filter(class_enrolled=klass)
		return render_to_response('setgrades.html',{'class':klass,'enrolled':enrolled})
	return HttpResponse("You don't have permission to view this page")

