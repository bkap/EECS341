from django.conf.urls.defaults import *
from views import login_page, hello
urlpatterns = patterns('',
	(r'login.html',login_page),
	(r'welcome.html',hello))
