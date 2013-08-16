from django.contrib import admin
from buggy.models import Project, Ticket, Comment

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)

class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ticket, TicketAdmin)
