from django import forms 
from main.models import Ticket

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('logged_by', 'status',)

class EngineerUpdateTicketForm(forms.ModelForm):
    CHOICES = (
            ('N', 'New'),
            ('U', 'Under Investigation'),
            ('R', 'Resolved'),
         )
    status =  forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Ticket
        fields = ['status', 'description', 'resolution']
