from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from events import views 
from django.urls import path
from events.views import profile, update_profile
from django.contrib.auth.views import LogoutView
from events.views import create_event, update_event, delete_event, view_events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/update/', update_profile, name='update_profile'),
    # path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('create_event/', create_event, name='create_event'),
    path('update_event/<int:event_id>/', update_event, name='update_event'),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    path('events/', views.view_events, name='view_events'),  # View all events
    path('events/update/<int:event_id>/', views.update_event, name='update_event'),  # Update specific event
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
