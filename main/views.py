from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView, UpdateView
from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here


def home(request):
    return render(request,'main/index.html')


class TicketCreate(CreateView):
    model = Ticket

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        group = Group.objects.get(name='Engineers')
        if group in self.request.user.groups.all():
            return super(TicketCreate, self).dispatch(*args, **kwargs)
        else:
            return redirect('index')

class TicketUpdate(UpdateView):
    model = Ticket

