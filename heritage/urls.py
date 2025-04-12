from django.urls import path
from . import views

urlpatterns = [
    #path('', views.welcome_view, name='welcome'),
    path('place/<slug:slug>/', views.place_detail, name='place_detail'),
    path('map/', views.map_view, name='map'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    #path('donate/', views.donate_view, name='donate'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('etiquette/', views.etiquette_view, name='etiquette'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('hidden-gems/', views.hidden_gems, name='hidden_gems'),
    path('submit/', views.submit_hidden_gem, name='submit_hidden_gem'),
    path('approved/', views.approved_hidden_gems, name='approved_hidden_gems'),
    path('filtered/', views.filtered_hidden_gems, name='filtered_hidden_gems'),

]
