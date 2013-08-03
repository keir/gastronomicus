from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'gastronomicus.views.home', name='home'),
    url(r'^adjacency/$', 'gastronomicus.views.adjacency', name='home'),
)
