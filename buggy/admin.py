from django.contrib import admin
from buggy.models import Project, Ticket, Comment, Status

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
    pass

admin.site.register(Status, StatusAdmin)

