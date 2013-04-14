from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',	
	url(r'^login/$', 'accounts.views.login', name='tts_login'),
	url(r'^overview/$', 'accounts.views.overview', name='overview'),
    # Examples:
    # url(r'^$', 'tts.views.home', name='home'),
    # url(r'^tts/', include('tts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
