from django import forms 
from main.models import Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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



class SupervisorUpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']





class registrationform(UserCreationForm):
    address=forms.CharField()
    phone=forms.CharField(max_length=200)

    class Meta:
        model = User
        fields=('first_name','last_name','username','password1','password2','email','phone','address')

    def save(self,commit=True):
        user = super(registrationform,self).save(commit=False)
        user.address = self.cleaned_data['address']
        user.phone=self.cleaned_data['phone']
        if commit:
            user.save()

        return user






