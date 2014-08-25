from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages

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