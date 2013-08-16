from django.db import models
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

STATUS_CHOICES = (
  (0, _("Opened")),
  (1, _("Confirmed")),
  (2, _("Waiting for code review")),
  (3, _("Waiting for verification")),
  (4, _("Fixed")),
  (5, _("Wont't fix")),
  (6, _("Closed")),
  (7, _("Invalid")),
)

PRIORITY_CHOICES = (
    (0, _('Low')),
    (1, _('Medium')),
    (2, _('High')),
    (4, _('Urgent')),
    (5, _('Critical')),
)

class Project(models.Model):

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    url = models.CharField(max_length=255, verbose_name=_('Repository URL'), blank=True)
    workflow = models.TextField(verbose_name=_('Workflow'), blank=True)

class Ticket(models.Model):


    project = models.ForeignKey(Project)
    
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="assignee")

    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=_('Status'))
    priority = models.IntegerField(choices=PRIORITY_CHOICES, verbose_name=_('Priority'))

    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated on'), auto_now=True)

    tags = TaggableManager(blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['-status', '-priority']


class Comment(models.Model):

    ticket = models.ForeignKey(Ticket)
    description = models.TextField(verbose_name=_('Description'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    # to register a change in the status of the ticket
    status_before = models.IntegerField(choices=STATUS_CHOICES, verbose_name=_('Old status'))
    status_after = models.IntegerField(choices=STATUS_CHOICES, verbose_name=_('New status'))

    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated on'), auto_now=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_on']

