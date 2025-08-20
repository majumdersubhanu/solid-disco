from django.shortcuts import render, get_object_or_404, redirect

from .forms import EnquiryForm
from .models import Hotel, Destination


def home(request):
    featured_hotels = Hotel.objects.filter(is_featured=True)
    featured_destinations = Destination.objects.filter(is_featured=True)
    context = {
        "featured_hotels": featured_hotels,
        "featured_destinations": featured_destinations,
    }
    return render(request, "home.html", context)


def destinations(request):
    destinations = Destination.objects.all()
    return render(request, "destinations.html", {"destinations": destinations})


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    return render(request, "destination_detail.html", {"destination": destination})


def hotels(request):
    hotels = Hotel.objects.all()
    return render(request, "hotels.html", {"hotels": hotels})


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    return render(request, "hotel_detail.html", {"hotel": hotel})


def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EnquiryForm()
    return render(request, "contact.html", {"form": form})
