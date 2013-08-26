from django.contrib import admin
from buggy.models import Project, Ticket, Comment, Status, Priority

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)

class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ticket, TicketAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'order')

admin.site.register(Status, StatusAdmin)

class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

admin.site.register(Priority, PriorityAdmin)
