from django.conf.urls import patterns, include, url
from djangobp.route import controller_resource_method_pattern, router
import jobs.controllers
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'accounts/', include('social_auth.urls')),
    (controller_resource_method_pattern, router(jobs.controllers)),

    # Examples:
    # url(r'^$', 'devjobs.views.home', name='home'),
    # url(r'^devjobs/', include('devjobs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
