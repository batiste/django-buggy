# Create your views here.
from buggy.models import Project, Ticket, Comment
from django.http import HttpResponse
from django.shortcuts import render_to_response

def projects(request):
    projects = Project.objects.all()
    return render_to_response('buggy/projects.html', {'projects': projects})

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    tickets = Ticket.object.filter(project=project)
    return render_to_response('buggy/project.html', 
        {'project': project, 'tickets':tickets})

def ticket(request, ticket_id):
    ticket = Ticket.object.get(id=ticket_id)
    project = ticket.project
    return render_to_response('buggy/ticket.html', 
        {'project': project, 'ticket':ticket})
