from django.db.models.signals import post_save
from .models import Ticket
from django.core.mail import send_mail
import requests


def notification(sender, instance, created, **kwargs):
    if created:

        engineer_email_id = instance.assigned_to.email
        client_email_id = instance.client.email
        engineer_email_subj = " Issue no: %s [%s] has been assigned to you " %(str(instance.id), instance.get_priority_display())
        client_email_subj = " Issue no: %s [%s] has been created  " %(str(instance.id), instance.get_priority_display())
        email_body = """

        Issue no     : %s
        Issue Name   : %s
        Client       : %s
        Assigend to  : %s
        Priority     : %s
        url          : %s

         """ % (str(instance.id), instance.name, instance.client.username, 
                instance.assigned_to.username, instance.get_priority_display(), 
                instance.get_absolute_url())

        sms_request = "http://bulksms.mysmsmantra.com:8080/WebSMS/SMSAPI.jsp?username=bhuvangates&password=bhuvan&sendername=bhuvan&mobileno=%s&message=%s" %(instance.client.profile.phone_number, client_email_subj)
        r = requests.get(sms_request)
        send_mail(engineer_email_subj, email_body, 'issuetrackingproject@gmail.com',[engineer_email_id])
        send_mail(engineer_email_subj, email_body,'issuetrackingproject@gmail.com',[client_email_id])



    if instance.status == 'V':
        client_email_subj = " Issue no: %s [%s] has been Resolved  " %(str(instance.id), instance.get_priority_display())
        email_body = """

        Issue no     : %s
        Issue Name   : %s
        Client       : %s
        Assigend to  : %s
        Priority     : %s
        url          : %s

         """ % (str(instance.id), instance.name, instance.client.username, 
                instance.assigned_to.username, instance.priority.get_priority_display(), 
                instance.get_absolute_url())
        
        send_mail(client_email_subj, email_body,'issuetrackingproject@gmail.com',[instance.client.email]) 

post_save.connect(notification, sender=Ticket)