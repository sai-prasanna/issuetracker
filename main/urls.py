from django.conf.urls import patterns, include, url
from .views import TicketCreate, TicketList, TicketDetail
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$','main.views.home',name="index"),
        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='login'),
        url(r'^logout/$', 'main.views.logout_view', name='logout'),
        url(r'^tickets/$', TicketList.as_view(), name='ticket_list'),
        url(r'^tickets/new/$', TicketCreate.as_view(), name='ticket_create'),
        url(r'^tickets/(?P<pk>[0-9]+)/$',TicketDetail.as_view(), name='ticket_detail'),


    )

