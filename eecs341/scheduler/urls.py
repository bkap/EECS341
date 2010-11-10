from django.conf.urls.defaults import *
from views import login, hello
urlpatterns = patterns('',
	(r'login.html',login),
	(r'welcome.html',hello))
