from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("destinations/", views.destinations, name="destinations"),
    path(
        "destinations/<slug:slug>/", views.destination_detail, name="destination_detail"
    ),
    path("hotels/", views.hotels, name="hotels"),
    path("hotels/<slug:slug>/", views.hotel_detail, name="hotel_detail"),
    path("contact/", views.contact, name="contact"),
]
