from django.conf.urls.defaults import *
from django.contrib import admin
import os.path
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
def location() :
	return os.path.abspath(os.path.dirname(__file__))
urlpatterns = patterns('',
    # Example:
     (r'^scheduler/', include('eecs341.scheduler.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
	 (r'^$', 'scheduler.views.lol'),
	 (r'^static/(.*)$','django.views.static.serve',{'document_root': location() + '/static/'}),
)
