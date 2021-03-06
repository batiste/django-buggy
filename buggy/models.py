from django.db import models
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.text import Truncator

class Project(models.Model):

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    url = models.CharField(max_length=255, verbose_name=_('Repository URL'), blank=True)
    workflow = models.TextField(verbose_name=_('Workflow'), blank=True)

    def get_absolute_url(self):
        return reverse('buggy.project', args=[str(self.id)])

    def __unicode__(self):
        return self.title

    def opened_tickets(self):
        return self.ticket_set.filter(Q(status__type="start") | Q(status__type="intermediate"))

    def resolved_tickets(self):
        return self.ticket_set.filter(status__type="end")

STATUS_TYPES = (
  ("start", _("Start")),
  ("intermediate", _("Intermediate")),
  ("end", _("Final")),
)

class Status(models.Model):
  
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    type = models.CharField(max_length=20, verbose_name=_('Type'), choices=STATUS_TYPES)
    order = models.PositiveIntegerField(default=5, help_text="Smaller first")

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
        ordering = ['order']

    def __unicode__(self):
        return self.name


class Priority(models.Model):
  
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    order = models.PositiveIntegerField(default=5, help_text="Smaller first")

    class Meta:
        verbose_name = _('Priority')
        verbose_name_plural = _('Priorities')
        ordering = ['order']

    def __unicode__(self):
        return self.name


class Ticket(models.Model):

    project = models.ForeignKey(Project)
    
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="assignee")

    status = models.ForeignKey(Status)
    priority = models.ForeignKey(Priority)

    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated on'), auto_now=True)

    duplicate = models.ForeignKey('self', blank=True, null=True)

    tags = TaggableManager(blank=True)
    
    def __unicode__(self):
        return Truncator(self.title).chars(30)

    def get_absolute_url(self):
        return reverse('buggy.ticket', args=[str(self.id)])

    def is_closed(self):
        return self.status.type == "end"
    
    def get_icon(self):
        if self.status.type == "intermediate":
            return "icon-cogs"
        if self.status.type == "end":
            return "icon-check"
        return "icon-bug"

    def get_style(self):
        if self.is_closed():
            return "background-color:#398439;color:#fff;"
        i = 0
        priorities = Priority.objects.order_by('-order')
        for priority in priorities:
            if priority == self.priority:
                break
            i = i + 1
        amount_of_red = i * (255 / len(priorities))
        return 'background-color:#%02X%02X%02X;' % (255, 255-amount_of_red, 255-amount_of_red)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['status__order', 'priority__order']


class Comment(models.Model):

    ticket = models.ForeignKey(Ticket)
    description = models.TextField(verbose_name=_('Description'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    # to register a change in the status of the ticket
    status_before = models.ForeignKey(Status, verbose_name=_('Old status'), 
        blank=True, null=True, related_name="status_before")
    status_after = models.ForeignKey(Status, verbose_name=_('New status'), 
        blank=True, null=True)

    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated on'), auto_now=True)

    def __unicode__(self):
        return Truncator(self.description).chars(30)

    def status_changed(self):
        stb = self.status_before
        sta = self.status_after
        if stb and sta and stb != sta:
            return 'The status has been changed from "%s" to "%s"' % (stb, sta)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_on']

