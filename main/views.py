from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Ticket
from .forms import CreateTicketForm, EngineerUpdateTicketForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from endless_pagination.views import AjaxListView
from django.contrib.messages.views import SuccessMessageMixin


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
# Create your views here


def home(request):
    return render(request,'main/index.html')


def logout_view(request):
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('index')

class TicketCreateView(SuccessMessageMixin, CreateView):
    model = Ticket
    form_class = CreateTicketForm
    success_message = "Ticket was created successfully"


    def get_form(self, form_class):
        form = super(TicketCreateView, self).get_form(form_class)
        form.fields['assigned_to'].queryset = User.objects.filter(groups__name='Engineers')
        form.instance.logged_by = self.request.user
        return form


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Helpdesk').exist():
            return super(TicketCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect('index')

class TicketListView(AjaxListView):
    model = Ticket
    context_object_name = "ticket_list"
    template_name = "ticket_list.html"
    paginate_by = 10



class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket'


class TicketUpdateView(SuccessMessageMixin, UpdateView):
    model = Ticket
    template_name_suffix = '_update_form'
    context_object_name = 'ticket'
    success_message = "Ticket was updated successfully"



    def get_form_class(self):
        if self.request.user.groups.filter(name='Engineers').exists():
            return EngineerUpdateTicketForm
        

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)
    