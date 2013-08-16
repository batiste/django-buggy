from django.conf.urls import patterns, url
from buggy.views import projects, project, ticket

urlpatterns = patterns('',
    url(r'^projects/$', project, name="buggy.projects"),
    url(r'^project/(?P<project_id>\d+)/$', projects, name="buggy.project"),
    url(r'^ticket/(?P<ticket_id>\d+)/$', ticket, name="buggy.ticket"),
)
