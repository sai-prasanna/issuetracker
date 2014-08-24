from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','main.views.home',name="index"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='login'),

    )