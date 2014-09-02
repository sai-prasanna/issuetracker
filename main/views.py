from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from endless_pagination.views import AjaxListView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.context_processors import csrf
from .models import Ticket, ClientProfile
from .forms import CreateTicketForm, EngineerUpdateTicketForm, SupervisorUpdateTicketForm, ClientRegistrationForm
from django.contrib.auth.models import Group


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():            
            user = form.save()
            user.groups.add(Group.objects.get(name="Client"))
            client = ClientProfile(user=user,address=form.cleaned_data['address'],phone_number=form.cleaned_data['phone_number'])
            client.save()
            messages.success(request,'Registered successfully and logged in ')
            return redirect('index')
    args={}
    args.update(csrf(request))
    args['form']=ClientRegistrationForm()

    return render(request,'main/register.html',args)





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
        form.fields['client'].queryset = User.objects.filter(groups__name='Client')
        form.fields['assigned_to'].queryset = User.objects.filter(groups__name='Engineer')
        form.instance.logged_by = self.request.user
        return form


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.filter(name='HelpDesk').exists():
            return super(TicketCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect('index')



class UserTicketListView(AjaxListView):
    model = Ticket
    context_object_name = "user_ticketlist"
    template_name = "main/user_ticket_list.html"
    page_template = "main/user_ticket_list_page.html"
    paginate_by = 10


    def get_queryset(self):
            if self.request.user.groups.filter(name='HelpDesk').exists():
                ticket_list = Ticket.objects.filter(logged_by = self.request.user)               
            elif self.request.user.groups.filter(name='Engineer').exists():
                ticket_list = Ticket.objects.filter(assigned_to = self.request.user)
            elif self.request.user.groups.filter(name='Client').exists():
                ticket_list = Ticket.objects.filter(client = self.request.user)
            elif self.request.user.groups.filter(name="Supervisor").exist():
                return Ticket.objects.all()
            return ticket_list


class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['is_supervisor'] = self.request.user.groups.filter(name='Supervisor').exists()
        return context


class TicketUpdateView(SuccessMessageMixin, UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    success_message = "Ticket was updated successfully"

    def get_form_class(self):
        ticket = self.get_object()
        if self.request.user.groups.filter(name='Engineer').exists() and ticket.assigned_to == self.request.user:
            return EngineerUpdateTicketForm
        elif self.request.user.groups.filter(name='HelpDesk').exists() and ticket.logged_by == self.request.user:
            self.template_name = 'main/ticket_form.html'
            return CreateTicketForm
        elif self.request.user.groups.filter(name='Supervisor').exists():
            self.template_name='main/ticket_supervisor_form.html'
            return SupervisorUpdateTicketForm
        else:
            return None

        

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.get_form_class():
            messages.error(self.request, 'Insufficient Permission to edit the Ticket')
            return redirect('index')
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)
    