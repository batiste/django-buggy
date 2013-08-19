from django.conf.urls import patterns, url

urlpatterns = patterns('buggy.views',
    url(r'^projects/$', "projects", name="buggy.projects"),
    url(r'^project/(?P<project_id>\d+)/$', "project", name="buggy.project"),
    url(r'^ticket/(?P<ticket_id>\d+)/$', "ticket", name="buggy.ticket"),
    url(r'^project/(?P<project_id>\d+)/ticket/create/$', "ticket_create", name="buggy.ticket-create"),
    url(r'^ticket/(?P<ticket_id>\d+)/edit/$', "ticket_edit", name="buggy.ticket-edit"),

)
