from django.db import models
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse


STATUS_CHOICES = (
  # start
  ("opened", _("Opened")),

  # intermediate
  ("confirmed", _("Confirmed")),
  ("waitreview", _("Waiting for code review")),
  ("waitverification", _("Waiting for verification")),
  (5, _("Verified in staging")),
  (6, _("Verified in production")),
  (8, _("Cannot reproduce")),

  # final
  (30, _("Fixed")),
  (31, _("Closed")),
  (32, _("Invalid")),
  (33, _("Won't fix")),
  (34, _("Duplicate")),
)

STATUS_TYPES = (
  ("start", _("Start")),
  ("intermediate", _("Intermediate")),
  ("end", _("Final")),
)

PRIORITY_CHOICES = (
    ('low', _('Low')),
    ('medium', _('Medium')),
    ('high', _('High')),
    ('urgent', _('Urgent')),
    ('critical', _('Critical')),
)

class Project(models.Model):

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    url = models.CharField(max_length=255, verbose_name=_('Repository URL'), blank=True)
    workflow = models.TextField(verbose_name=_('Workflow'), blank=True)

    def get_absolute_url(self):
        return reverse('buggy.project', args=[str(self.id)])

    def __unicode__(self):
        return self.title

class Status(models.Model):
  
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    type = models.CharField(max_length=20, verbose_name=_('Type'), choices=STATUS_TYPES)

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def __unicode__(self):
        return self.name

class Ticket(models.Model):

    project = models.ForeignKey(Project)
    
    title = models.CharField(max_length=25, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="assignee")

    status = models.ForeignKey(Status, default=Status.objects.get(name="Opened"))
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=25, verbose_name=_('Priority'), default='medium')

    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated on'), auto_now=True)

    duplicate = models.ForeignKey('self', blank=True, null=True)

    tags = TaggableManager(blank=True)
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('buggy.ticket', args=[str(self.id)])
    
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['-status', '-priority']


class Comment(models.Model):

    ticket = models.ForeignKey(Ticket)
    description = models.TextField(verbose_name=_('Description'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    # to register a change in the status of the ticket
    status_before = models.ForeignKey(Status, verbose_name=_('Old status'), blank=True, null=True, related_name="status_before")
    status_after = models.ForeignKey(Status, verbose_name=_('New status'), blank=True, null=True)

    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated on'), auto_now=True)

    def __unicode__(self):
        return self.description[0:30]

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_on']

