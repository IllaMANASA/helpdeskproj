from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('ticket/<int:pk>/edit/', views.ticket_edit, name='ticket_edit'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
