from django.conf.urls import patterns, include, url
from .views import TicketCreate
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$','main.views.home',name="index"),
        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='login'),
        url(r'^ticket/create/$', TicketCreate.as_view(), name='ticket_create'),
    )

