from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Ticket
from .forms import CreateTicketForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here


def home(request):
    return render(request,'main/index.html')


def logout_view(request):
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('index')

class TicketCreate(CreateView):
    model = Ticket
    success_url="/tickets"
    form_class = CreateTicketForm

    def get_form(self, form_class):
        form = super(TicketCreate, self).get_form(form_class)
        form.fields['assigned_to'].queryset = User.objects.filter(groups__name='Engineers')
        form.instance.logged_by = self.request.user
        return form


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        group = Group.objects.get(name='Helpdesk')
        if group in self.request.user.groups.all():
            return super(TicketCreate, self).dispatch(*args, **kwargs)
        else:
            return redirect('index')

class TicketList(ListView):
    model = Ticket
    context_object_name = "ticket_list"
    paginate_by = 10


class TicketDetail(DetailView):
    model = Ticket
    context_object_name = 'ticket'