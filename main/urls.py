from django.conf.urls import patterns, include, url
from .views import TicketCreateView, TicketDetailView, TicketUpdateView, UserTicketListView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$','main.views.home',name="index"),
        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='login'),
        url(r'^logout/$', 'main.views.logout_view', name='logout'),
        url(r'^tickets/$', UserTicketListView.as_view(), name='ticket_list'),
        url(r'^tickets/new/$', TicketCreateView.as_view(), name='ticket_create'),
        url(r'^tickets/(?P<pk>[0-9]+)/$',TicketDetailView.as_view(), name='ticket_detail'),
        url(r'^tickets/(?P<pk>[0-9]+)/update/$',TicketUpdateView.as_view(), name='ticket_update'),
        url(r'^register/$','main.views.register',name='register'),
    )

urlpatterns += staticfiles_urlpatterns()
