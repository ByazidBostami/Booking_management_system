from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.profile, name='profile'),
    path('create_event/', views.create_event, name='create_event'),
    path('book_event/<int:event_id>/', views.book_event, name='book_event'),
    path('booked_events/', views.booked_events, name='booked_events'),
    path('register/', views.register, name='register'), 
]
