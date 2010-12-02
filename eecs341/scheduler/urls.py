from django.conf.urls.defaults import *
from views import login_page, hello,search_form, searchresults, getgrades, set_grades, enroll_in_class
urlpatterns = patterns('',
	(r'^login.html',login_page),
	(r'^welcome.html',hello),
	(r'^searchform.html',search_form),
	(r'^search.html',searchresults),
	(r'^grades.html',getgrades),
	(r'^setgrades.html',set_grades),
	(r'^enroll.html', enroll_in_class),
	)
