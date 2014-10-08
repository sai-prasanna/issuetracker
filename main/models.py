from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

class ClientProfile(models.Model):
    """
    Model to store client profile .
    address,company name, phone number as fields

    """

    user = models.OneToOneField(User, related_name='profile')
    address = models.TextField()
    company_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
   
    def __unicode__(self):
        return u"%s : %s " %(self.user.username, self.company_name)

class Ticket(models.Model):
    """
        Model to store  ticket
    """

    PRIORITY = (
            ('L', 'Low'),
            ('N', 'Normal'),
            ('H', 'High'),
         )

    SLA = {'L':24, 'N':72, 'H':120}
    STATUS = (
            ('N', 'New'),
            ('U', 'Under Investigation'),
            ('R', 'Resolved'),
            ('C', 'Closed'),

         )
    client = models.ForeignKey(User, related_name='ticket')
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    logged_by = models.ForeignKey(User, related_name='logged_ticket')
    assigned_to = models.ForeignKey(User, related_name='assigned_ticket')
    priority = models.CharField(max_length=1, choices=PRIORITY, default=PRIORITY[1][0])
    status = models.CharField(max_length=1,choices=STATUS, default=STATUS[0][0])
    estimated_completion_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('ticket_detail', args=[str(self.id)])

    def __unicode__(self):
        return str(self.id) + ':' + self.name + ":" + unicode(self.client) 




