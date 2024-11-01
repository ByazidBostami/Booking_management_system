from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Event, Booking
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view."""
    return render(request, 'events/profile.html')


@login_required
def update_profile(request):
    """Update user profile view."""
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()  # Save the updated user information
        return redirect('profile')  # Redirect to the profile page after updating
    return render(request, 'events/update_profile.html')


def homepage(request):
    """Homepage with event listings and search functionality."""
    query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    events = Event.objects.all()
    
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(date__icontains=query) |
            Q(location__icontains=query)
        )
    
    if category_filter:
        events = events.filter(category=category_filter)
    
    user_booked_events = Booking.objects.filter(user=request.user).values_list('event_id', flat=True) if request.user.is_authenticated else []

    return render(request, 'events/homepage.html', {
        'events': events,
        'query': query,
        'category_filter': category_filter,
        'user_booked_events': user_booked_events,
    })


@login_required
def create_event(request):
    """Create an event view."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Set the creator to the logged-in user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('homepage')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def book_event(request, event_id):
    """Book an event view."""
    event = get_object_or_404(Event, id=event_id)

    if event.is_fully_booked():
        messages.warning(request, "This event is fully booked.")
    elif Booking.objects.filter(user=request.user, event=event).exists():
        messages.info(request, "You have already booked this event.")
    else:
        Booking.objects.create(user=request.user, event=event)
        event.bookings_count += 1
        event.save()
        messages.success(request, "Event booked successfully!")
    
    return redirect('homepage')


@login_required
def booked_events(request):
    """List of events booked by the user."""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/booked_events.html', {'bookings': bookings})


@login_required
# def update_event(request, event_id):
#     """Update an event view."""
#     event = get_object_or_404(Event, id=event_id, created_by=request.user)
    
#     if request.method == 'POST':
#         form = EventForm(request.POST, instance=event)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Event updated successfully!")
#             return redirect('homepage')
#     else:
#         form = EventForm(instance=event)
    
#     return render(request, 'events/update_event.html', {'form': form, 'event': event})

def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the current user is the creator of the event
    if event.created_by != request.user:
        return HttpResponseForbidden("You do not have permission to edit this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('view_events')  # Redirect after successful update
    else:
        form = EventForm(instance=event)

    return render(request, 'events/update_event.html', {
        'form': form,
        'event': event
    })

@login_required
# def delete_event(request, event_id):
#     """Delete an event view."""
#     event = get_object_or_404(Event, id=event_id, created_by=request.user)

#     if request.method == 'POST':
#         event.delete()
#         messages.success(request, "Event deleted successfully!")
#         return redirect('homepage')
    
#     return render(request, 'events/delete_event.html', {'event': event})
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the current user is the creator of the event
    if event.created_by != request.user:
        return HttpResponseForbidden("You do not have permission to delete this event.")

    if request.method == 'POST':
        event.delete()  # Delete the event if the user is the creator
        return redirect('view_events')  # Redirect to the view events page after deletion

    return render(request, 'events/delete_event.html', {'event': event})


def view_events(request):
    """Publicly view all events."""
    events = Event.objects.all()
    return render(request, 'events/view_events.html', {'events': events})
