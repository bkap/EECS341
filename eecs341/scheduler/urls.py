from django.conf.urls.defaults import *
from views import login_page, hello,search_form
urlpatterns = patterns('',
	(r'login.html',login_page),
	(r'welcome.html',hello),
	(r'search.html',search_form),)
