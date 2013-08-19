from django.forms import ModelForm
from buggy.models import Ticket, Comment


class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ["author", "project"]


class EditTicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ["author", "project"]


class EditTicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ["author", "project"]

class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["author", "ticket", "status_before"]

