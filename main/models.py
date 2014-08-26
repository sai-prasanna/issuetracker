from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
   
    def __unicode__(self):
        return self.name

class Ticket(models.Model):
    PRIORITY = (
            ('L', 'Low'),
            ('N', 'Normal'),
            ('H', 'High'),
         )
    STATUS = (
            ('N', 'New'),
            ('U', 'Under Investigation'),
            ('R', 'Resolved'),
            ('V', 'Verified'),

         )
    client = models.ForeignKey(Client, related_name='ticket')
    ticket_no = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    logged_by = models.ForeignKey(User, related_name='logged_ticket')
    assigned_to = models.ForeignKey(User, related_name='assigned_ticket')
    priority = models.CharField(max_length=1, choices=PRIORITY)
    status = models.CharField(max_length=1,choices=STATUS)
    time_elapsed = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    
    def get_fields(self):
        li=[]
        for field in Ticket._meta.fields:
            li.append((field.verbose_name, field.value_to_string(self)))
        return li

    def __unicode__(self):
        return self.ticket_no + ':' + self.name + ":" + unicode(self.client) 




