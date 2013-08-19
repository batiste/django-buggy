# Create your views here.
from buggy.models import Project, Ticket, Comment
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from buggy.forms import CreateTicketForm, EditTicketForm, CreateCommentForm
from django.core.urlresolvers import reverse


def projects(request):
    projects = Project.objects.all()
    return render_to_response('buggy/projects.html', {'projects': projects})

def project(request, project_id):

    project = Project.objects.get(id=project_id)
    options = {'show_all':False, 'only_assigned':False}
    key = 'buggy_project_'+str(project.id)

    if request.method == "POST":
        options['only_assigned'] = True if request.POST.get("only_assign_to_me", False) else False
        options['show_all'] = True if request.POST.get("show_resolved", False) else False
        request.session[key] = options

    if request.session.has_key(key):
        options = request.session[key]

    if options['show_all']:
        tickets = Ticket.objects.filter(project=project)
    else:
        tickets = project.opened_tickets()

    if options['only_assigned']:
        tickets = tickets.filter(assignee=request.user)

    context = RequestContext(request, {
        'project': project,
        'tickets':tickets, 
        'options':options
    })

    return render_to_response('buggy/project.html', context)

def ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    project = ticket.project

    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.status_before = ticket.status
            comment.save()
            if comment.status_after and comment.status_after != ticket.status:
                ticket.status = comment.status_after
                ticket.save()
            return http.HttpResponseRedirect(".")
    else:
        form = CreateCommentForm()

    comments = Comment.objects.filter(ticket=ticket)

    context = RequestContext(request, {
        'ticket': ticket, 
        'form':form, 'project':project, 'comments': comments
    })
  
    return render_to_response('buggy/ticket.html', context)

def ticket_create(request, project_id):

    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.project = project
            ticket.author = request.user
            ticket.save()
            return http.HttpResponseRedirect(
                reverse("buggy.project", args=(project.id,)))
    else:
        form = CreateTicketForm()

    return render_to_response('buggy/ticket_create.html', 
        RequestContext(request, {'project': project, 'form':form}))

def ticket_edit(request, ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)
    project = ticket.project

    if request.method == 'POST':
        form = EditTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return http.HttpResponseRedirect(
                reverse("buggy.ticket", args=(ticket.id,)))
    else:
        form = EditTicketForm(instance=ticket)

    return render_to_response('buggy/ticket_edit.html', 
        RequestContext(request, {'ticket': ticket, 'form':form, 'project':project}))


