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
from datetime import datetime, timedelta
from django.utils import timezone

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


def register(request):
    """ 
    View for Client registration

    """
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():            
            user = form.save()
            user.groups.add(Group.objects.get(name="Client"))
            client = ClientProfile(user=user,address=form.cleaned_data['address'],phone_number=form.cleaned_data['phone_number'])
            client.save()
            messages.success(request,'Registered successfully and please login')
            return redirect('index')
    args={}
    args.update(csrf(request))
    args['form']=ClientRegistrationForm()

    return render(request,'main/register.html',args)


def home(request):
    """
        View for homepage, with ticket count in context 

    """
    ticket_logged_count = Ticket.objects.all().count()
    ticket_resolved_count = Ticket.objects.filter(status='C').count()
    args = {}
    args['ticket_count'] = ticket_logged_count
    args['ticket_resolved_count'] = ticket_resolved_count

    return render(request,'main/index.html', args)


def logout_view(request):
    """
        View to logout 
    """
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
        return form
    
    def form_valid(self, form):
        form.instance.logged_by = self.request.user
        form.instance.date_time = timezone.now()
        hours_sla = Ticket.SLA[form.instance.priority]
        form.instance.estimated_completion_time = form.instance.date_time + timedelta(hours=hours_sla)
        return super(TicketCreateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.filter(name='HelpDesk').exists():
            return super(TicketCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect('index')



class UserTicketListView(AjaxListView):
    """
        Paginated view to list issues.Issues are listed based on group to which user belongs to and wether he/she
        has permission to view the ticket
    """
    model = Ticket
    context_object_name = "user_ticket_list"
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
            elif self.request.user.groups.filter(name='Supervisor').exists():
                return Ticket.objects.all()
            return ticket_list


class TicketDetailView(DetailView):
    """
        View for displaying Single ticket details
    """
    model = Ticket
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        ticket = self.get_object()
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['is_supervisor'] = self.request.user.groups.filter(name='Supervisor').exists()
        timedelta_until_ect = ticket.estimated_completion_time - timezone.now()
        context['time_until_etc'] = timedelta_until_ect.total_seconds() // 3600

        return context


class TicketUpdateView(SuccessMessageMixin, UpdateView):
    """
    View for Updating ticket,it dynamicaly shows form based on user prievelege to update the ticket

    """
    model = Ticket
    context_object_name = 'ticket'
    success_message = "Ticket was updated successfully"

    def get_form_class(self):
        ticket = self.get_object()
        if self.request.user.groups.filter(name='Engineer').exists() and ticket.assigned_to == self.request.user:
            self.template_name = 'main/ticket_engineer_update_form.html'
            return EngineerUpdateTicketForm
        elif self.request.user.groups.filter(name='HelpDesk').exists() and ticket.logged_by == self.request.user:
            self.template_name = 'main/ticket_form.html'
            return CreateTicketForm
        elif self.request.user.groups.filter(name='Supervisor').exists():
            self.template_name='main/ticket_supervisor_update_form.html'
            return SupervisorUpdateTicketForm
        else:
            return None

    def get_form(self, form_class):
        form_class = self.get_form_class()
        form = super(TicketUpdateView, self).get_form(form_class)
        if form_class == EngineerUpdateTicketForm or form_class == SupervisorUpdateTicketForm :
            form.fields['assigned_to'].queryset = User.objects.filter(groups__name='Engineer')

        return form
        

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.get_form_class():
            messages.error(self.request, 'Insufficient Permission to edit the Ticket')
            return redirect('index')
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)
    