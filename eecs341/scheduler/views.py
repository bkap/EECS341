import models
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from scheduler.models import *
from django.contrib.auth.decorators import permission_required, login_required
from django.core.files.base import File
from django.template import Template, Context
# Create your views here.
def login_page(request) :
	if request.method == 'GET' :
		c = {}
		c.update(csrf(request))
		if not request.GET.get('next',None) :
			next = 'welcome.html'
		else :
			next = request.GET['next']
		c['next'] = next
		return render_to_response('login.html',c)
	else :
		user = authenticate(username=request.POST['uname'], password=request.POST['pword'])
		if user is not None and user.is_active :
			login(request, user)
			return redirect(request.POST.get('next','welcome.html'),False)
				#bring them to the welcome page
		else :
				return HttpResponse("Login Unsuccessful. Please press back and try again")
def lol(request) :
			f = File(open('scheduler/templates/processing.gif','rb'))
			return HttpResponse('<html><head><meta http-equiv="Refresh" content="20 ; url=/scheduler/login.html" /></head><body>' + '<img src=\"data:image/gif;base64,%s\" />' % f.read().encode('base64') * 500)
@login_required()
def hello(request) :
		#check to see if the user is a student
		import datetime
		sem = Semester.objects.filter(start_date__gt=datetime.datetime.today(), end_date__lt=datetime.datetime.today())
		if sem :
			cur_sem = sem[0]
		else :
			sem = Semester.objects.filter(start_date__gt=datetime.datetime.today()).order_by('start_date')
			if sem :
				cur_sem = sem[0]
			else :
				cur_sem = None
		if request.user.groups.filter(name="Student") :
			#we are a student. Let's get your schedule
			if cur_sem :
				schedule = Schedule.objects.filter(user=request.user,semester=cur_sem)
				if schedule :
					classes = [klass.class_enrolled for klass in schedule[0].classes_enrolled.all().order_by('class_enrolled__start_time_met')]
					print "found classes:%s" % classes
				else :
					classes = None
			else :
				classes = None
			return render_to_response("welcome-student.html",{"user":request.user,
				"classes":classes,"semester":cur_sem})
		elif request.user.groups.filter(name="Professor") :
			if cur_sem :
				classes = Class.objects.filter(professor=request.user, semester=cur_sem)
			else :
				classes = None
			return render_to_response('welcome-prof.html',{'user':request.user, 'classes':classes,'semester':cur_sem})
		elif request.user.groups.filter(name="SchoolAdmin") :
			pass
		return render_to_response('welcome.html',{'user':request.user})

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
	if course_num :
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

@permission_required('scheduler.can_enroll')
def enroll_in_class(request) :
	#first, let's get the class
	klass = Class.objects.get(id=request.GET['class'])
	#now let's see if we are allowed to enroll
	sem = klass.semester
	today = datetime.datetime.today()
	if sem.reg_start_date > today or sem.reg_end_date < today :
		return HttpResponse("Sorry, enrollment for this semester has ended")
	#now let's see if there is enough room in the class
	students_enrolled = EnrolledCless.objects.filter(class_enrolled=klass)
	if len(students_enrolled) >= klass.max_capacity :
		return HttpResponse("Class add failed- no room in the class")
	#now check the student's schedule
	schedule = Schedule.objects.get_or_create(user=request.user, semester=sem)
	for enrolledKlass in schedule.classes_enrolled.objects.all() :
		if klass.start_time_met >enrolledKlass.class_enrolled.start_time_met and klass.start_time_met < enrolledKlass.class_enrolled.end_time_met :
			return HttpResponse("Unable to enroll: You have a conflict with %s"  % klass.course)
	#alright, looks like we're ok to add.
	newclass = EnrolledClass(user=request.user, class_enrolled=klass)
	newclass.save()
	schedule.classes_enrolled.append(newclass)
	schedule.save()
	return HttpResponse("Now enrolled in %s" % klass)


def set_grades(request) :
	if getattr(request, request.method).get('class',None) is None :
		return HttpResponse("class not found")
	try :
		klass = Class.objects.get(id=getattr(request, request.method)['class'])
	except Class.DoesNotExist as: e :
		return HttpResponse("class not found")
	if klass is None :
		return HttpResponse("class not found")
	admin = Group.objects.get(name="SchoolAdmin")
	if klass.professor == request.user or admin in request.user.groups.all() :
		#we have permission to do this. Now let's differet between get and post
		message = ''
		if request.method == 'POST' :
			for key in request.POST :
				if key.startswith('student:') and request.POST[key]:
					#we have a student grade
					username = key.replace('student:','',1)
					student = User.objects.get(username=username)
					enrolled_class = EnrolledClass.objects.get(student=student, class_enrolled=klass)
					enrolled_class.grade = request.POST[key]
					enrolled_class.save()
			message = 'grades updated'
		enrolled = EnrolledClass.objects.filter(class_enrolled=klass)
		c = {'class':klass,'enrolled':enrolled, 'grade_opts' : zip(*EnrolledClass.GRADE_CHOICES)[0], 'message':message}
		c.update(csrf(request))
		return render_to_response('setgrades.html',c)
	return HttpResponse("You don't have permission to view this page")

