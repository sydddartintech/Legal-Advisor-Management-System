"""
URL configuration for legal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
 path('enquiry/',views.enquiry,name='enquiry'),
 path('send_enquiry/',views.send_enquiry,name='send_enquiry'),
 path('ask_question/',views.ask_question,name='ask_question'),
 path('save_question/',views.save_question,name='save_question'),
 path('contact/',views.contact,name='contact'),
 path('login/',views.login,name='login'),
    path('check_login/',views.check_login,name='check_login'),
    path('administrator/',include('administrator.urls')),
    path('change_password/',views.change_password,name='change_password'),
    path('update_password/',views.update_password,name='update_password'),
    path('logout/',views.logout,name='logout'),
    path('advocate/', include('advocate.urls')),
    path('forgot/',views.forgot,name='forgot'),
    path('otp/',views.otp,name='otp'),
    path('new_password/',views.new_password,name='new_password'),
    path('email_verify/',views.email_verify,name='email_verify'),
     path('client/', include('client.urls')),
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

