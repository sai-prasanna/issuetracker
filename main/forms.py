from django import forms 
from main.models import Ticket

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('logged_by', 'status',)
