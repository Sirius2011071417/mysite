"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.contrib.auth import views as auth_views
import books.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^django/$', views.django),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/register/$', views.register),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/changepassword/(?P<username>\w+)/$', views.changepassword),
    url(r'^contact/$', views.contact),
    url(r'^contact/success/$', views.contact_success),
    url(r'^accounts/messages/(?P<username>\w+)/$', views.mylist),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/success/$', views.upload_success, name='upload_success'),
    url(r'^algo/$', views.algo, name='algo'),

]
