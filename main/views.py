from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Ticket,Client
from .forms import CreateTicketForm, EngineerUpdateTicketForm,SupervisorUpdateTicketForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from endless_pagination.views import AjaxListView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.context_processors import csrf
from main.forms import registrationform
from django.http import HttpResponseRedirect
import socket,errno,time

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
# Create your views here
def register(request):
    if request.method == 'POST':
        form = registrationform(request.POST,request.FILES)
        

        if form.is_valid():
            print form.cleaned_data.get('address')
            print form.cleaned_data.get('phone')
            address=form.cleaned_data.get('address')
            phone=form.cleaned_data.get('phone')
            user = form.save()
            client = Client(user=user,address=address,phone=phone)
            client.save()            
            user.groups.add(Group.objects.get(name='Client'))
            return HttpResponseRedirect('/register_success/')

    args={}
    args.update(csrf(request))
    args['form']=registrationform()
    print args
    return render(request,'main/register.html',args)


def register_success(request):
    messages.success(request,'Registered successfully')
    return render(request,'main/index.html')


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
        if self.request.user.groups.filter(name='HelpDesk').exists():
            return super(TicketCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect('index')

class TicketListView(AjaxListView):
    model = Ticket
    context_object_name = "ticket_list"
    template_name = "ticket_list.html"
    paginate_by = 10


class UserTicketView(AjaxListView):
    model = Ticket
    context_object_name = "user_ticketlist"
    template_name = "main/user_ticketlist.html"
    page_template = "main/user_ticketlist_page.html"
    paginate_by = 2


    def get_queryset(self):
        customerusergroups = self.request.user.groups.all()
        for group in customerusergroups:
            try:
                if str(group) == 'HelpDesk':
                    loggeduser = self.request.user
                    log = User.objects.filter(username = loggeduser)
                    ticketlist = Ticket.objects.filter(logged_by = log) 
                    
                elif str(group) == 'Engineers':
                    assigneduser = self.request.user
                    assigned = User.objects.filter(username = loggeduser)
                    ticketlist = Ticket.objects.filter(assigned_to = assigned)

                elif str(group) == 'Client':
                    customer = self.request.user
                    customercreated = User.objects.filter(username = customer)
                    ticketlist = Ticket.objects.filter(client = customercreated)


                return ticketlist

            except socket.error,e:
                print 'socketerror'
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
        elif self.request.user.groups.filter(name='HelpDesk').exists():
            self.template_name = 'main/ticket_form.html'
            return CreateTicketForm
        elif self.request.user.groups.filter(name='Supervisor').exists():
            self.template_name='main/ticket_supervisorform.html'
            return SupervisorUpdateTicketForm

        

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)
    