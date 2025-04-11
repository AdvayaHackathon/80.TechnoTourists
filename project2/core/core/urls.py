"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from heritage import views as hv
from heritage import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hv.welcome, name='welcome'),
    path('', include('heritage.urls')),
    path('register/', hv.register_view, name='register'),
    path('login/', hv.login_view, name='login'),
    path('logout/', hv.logout_view, name='logout'),
    path('dashboard/', hv.dashboard, name='dashboard'),
    path('map/', hv.map_view, name='map'),
    path('donate/', hv.donate, name='donate'),
    path('etiquette/', hv.etiquette_view, name='etiquette'),
    path('chatbot/', hv.chatbot_view, name='chatbot'),
    path('calendar/', hv.calendar_view, name='calendar'),
    path('submit-hidden-gem/', views.submit_hidden_gem, name='submit_hidden_gem'),


]

