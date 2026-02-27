from django.shortcuts import render, get_object_or_404
from .models import Event


def event_list(request):
    events = Event.objects.filter(do_not_show=False)
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/event_detail.html", {"event": event})

