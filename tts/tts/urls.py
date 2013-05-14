from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',	
	url(r'^$', 'timetrack.views.index', name='index'),
	url(r'^login/$', 'accounts.views.signin', name='tts_login'),
	# url(r'^overview/$', 'accounts.views.overview', name='overview'),
	url(r'^project/(?P<slug>[-_a-zA-Z0-9]+)/$', 'timetrack.views.project', name='project'),
    url(r'^common/$', 'accounts.views.common', name='common'),
    url(r'^request/$', 'timetrack.views.ooo_request', name='ooo_request'),
    url(r'^new-request/$', 'timetrack.views.new_request', name='new_request'),
    url(r'^track-time/(?P<taskid>\d+)/$', 'timetrack.views.track_time', name='track_time'),
    url(r'^worklog/$', 'timetrack.views.worklog', name='worklog'),
    url(r'^worklog/edit/(?P<id>\d+)/$', 'timetrack.views.worklog_edit', name='worklog_edit'),
    url(r'^reports/$', 'timetrack.views.reports', name='reports'),
    url(r'^import/$', 'timetrack.views.export', name='export'),
    #url(r'^management/$'),

    # Examples:
    # url(r'^$', 'tts.views.home', name='home'),
    # url(r'^tts/', include('tts.foo.urls')),

    url(r'^tasks/$', 'timetrack.views.tasks', name='tasks'),
    url(r'^profile/(?P<id>\d+)/$', 'accounts.views.profile', name='profile'),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),


)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()