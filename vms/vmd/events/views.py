from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Category, Event
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.db import models
from django.db.models import Count
from io import BytesIO
import matplotlib.pyplot as plt
from django.http import HttpResponse


def create_event(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')

        # Retrieve the Category object
        category = Category.objects.get(pk=category_id)

        # Create the Event object
        event = Event.objects.create(
            name=name,
            category=category,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            description=description,
            location=location,
            organizer=organizer
        )

        # Redirect to the event list page
        return redirect('events:category_list')
    else:
        categories = Category.objects.all()
        return render(request, 'create_event.html', {'categories': categories})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        # Update event fields based on form data
        event.name = request.POST.get('name')
        event.start_date = request.POST.get('start_date')
        event.end_date = request.POST.get('end_date')
        event.priority = request.POST.get('priority')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.organizer = request.POST.get('organizer')
        event.save()
        return redirect('events:category_list')
    else:
        # Render update event page with event data
        return render(request, 'update_event.html', {'event': event})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            print(f"Event found: {event.name}")  # Debugging line
            event.delete()
            messages.success(request, "Event deleted successfully.")
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
            print("Event does not exist")  # Debugging line
 
    return redirect('events:category_list')

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('events:category_list')
    return render(request, 'create_category.html')


# def delete_category(request, category_id):
#     category = Category.objects.get(pk=category_id)
#     if category.event_set.exists():
#         messages.error(
#             request, "You cannot delete this category as it contains events.")
#     else:
#         category.delete()
#         messages.success(request, "Category deleted successfully.")
#     return redirect('category_list')

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    # Check if category has related events
    if category.event_set.exists():
        messages.error(request, "You cannot delete this category as it contains events.")
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")

    return redirect('events:category_list')

def category_events(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    events = category.event_set.all()
    return render(request, 'category_events.html', {'category': category, 'events': events})


def event_chart(request):
    categories = Event.objects.values('category__name').annotate(count=models.Count('category'))

    if not categories:
        return HttpResponse("No events so far.", content_type="text/plain")

    labels = [cat['category__name'] for cat in categories]
    data = [cat['count'] for cat in categories]

    fig, ax = plt.subplots()
    ax.set_title("Event Categories Distribution")

    formatted_labels = [f"{label}\n {count} events" for label, count in zip(labels, data)]

    ax.pie(data, labels=formatted_labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode image to base64 so it can be embedded in HTML
    import base64
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Render the HTML page with the chart image
    return render(request, 'event_chart.html', {'chart': img_str})