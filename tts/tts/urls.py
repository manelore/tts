from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',	
	url(r'^$', 'timetrack.views.index', name='index'),
	url(r'^login/$', 'accounts.views.login', name='tts_login'),
	url(r'^overview/$', 'accounts.views.overview', name='overview'),

    # Examples:
    # url(r'^$', 'tts.views.home', name='home'),
    # url(r'^tts/', include('tts.foo.urls')),

    url(r'^tasks/$', 'timetrack.views.tasks', name='tasks'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
