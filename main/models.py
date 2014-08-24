from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

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
    date_time = models.DateTimeField()
    logged_by = models.CharField(max_length=200)
    assigned_to = models.CharField(max_length=200)
    priority = models.CharField(max_length=1, choices=PRIORITY)
    time_elapsed = models.DateTimeField()
    description = models.TextField()
    resolution = models.TextField()




