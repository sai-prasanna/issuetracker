from django import forms 
from main.models import Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateTicketForm(forms.ModelForm):
    """
        Form for helpdesk executive to create/update a  ticket
    """
    class Meta:
        model = Ticket
        fields = ('client', 'name', 'assigned_to', 'priority', 'description')

class EngineerUpdateTicketForm(forms.ModelForm):
    """
        Form for engineer to create and update ticket
    """

    CHOICES = (
            ('N', 'New'),
            ('U', 'Under Investigation'),
            ('R', 'Resolved'),
         )
    status =  forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Ticket
        fields = ['status', 'description', 'resolution', 'assigned_to']



class SupervisorUpdateTicketForm(forms.ModelForm):
    """
        Form for supervisor to update ticket.

    """

    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to']


class ClientRegistrationForm(UserCreationForm):
    """
    Form for client registration

    """

    address = forms.CharField()
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    class Meta:
        model = User
        fields=('first_name','last_name','username','password1','password2','email')






