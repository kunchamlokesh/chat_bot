"""rasadjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rasaweb import views
from django.urls import include, re_path

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^api/get_answer/$', views.Get_Answer.as_view()),
    re_path(r'^api/create_ticket/$', views.Create_Ticket.as_view()),
    re_path(r'^api/create_ticket/(?P<inc>[\w\-]+)/$', views.Create_Ticket.as_view()),
    re_path(r'^api/machine_rec/$', views.Machine_Recommendation.as_view()),
    re_path(r'^api/get_answer/(?P<question>[\w\s]+)/$', views.Get_Answer.as_view()),
    re_path('^$', include('rasaweb.urls')),
    re_path('accounts/', include('django.contrib.auth.urls')),

]
