from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from phonenumber_field.modelfields import PhoneNumberField


class Hotel(models.Model):
    """
    Represents a hotel listing in the database.
    """

    name = models.CharField(max_length=200, help_text="The name of the hotel.")
    # The description field is now a RichTextField for WYSIWYG editing
    description = CKEditor5Field(
        help_text="A detailed description of the hotel, including itinerary and details."
    )
    address = models.CharField(
        max_length=255, help_text="The physical address of the hotel."
    )
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Cost for a one-night stay."
    )
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, help_text="Star rating from 1.0 to 5.0."
    )
    amenities = models.TextField(
        help_text="List of amenities, separated by commas (e.g., Wi-Fi, Pool, Gym)."
    )
    # This is now the main "cover" image
    image = models.ImageField(
        upload_to="hotel_images/",
        help_text="The main representative (cover) image of the hotel.",
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="A unique slug for the hotel URL, generated from the name.",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Mark as true to feature this hotel on the homepage."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.city}"


class HotelImage(models.Model):
    """
    Represents an additional image for a Hotel.
    """

    hotel = models.ForeignKey(Hotel, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="hotel_images/gallery/")
    caption = models.CharField(
        max_length=200, blank=True, help_text="Optional caption for the image."
    )

    def __str__(self):
        return f"Image for {self.hotel.name}"


class Destination(models.Model):
    """
    Represents a travel destination.
    """

    name = models.CharField(
        max_length=200, help_text="The name of the destination (e.g., Paris, Goa)."
    )
    # The description field is now a RichTextField
    description = CKEditor5Field(
        help_text="A captivating description of the destination, including itinerary and details."
    )
    country = models.CharField(max_length=100)
    best_time_to_visit = models.CharField(
        max_length=100, help_text="e.g., 'October to March'"
    )
    # This is now the main "cover" image
    image = models.ImageField(
        upload_to="destination_images/",
        help_text="The main representative (cover) image of the destination.",
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="A unique slug for the destination URL, generated from the name.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as true to feature this destination on the homepage.",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country}"


class DestinationImage(models.Model):
    """
    Represents an additional image for a Destination.
    """

    destination = models.ForeignKey(
        Destination, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="destination_images/gallery/")
    caption = models.CharField(
        max_length=200, blank=True, help_text="Optional caption for the image."
    )

    def __str__(self):
        return f"Image for {self.destination.name}"


class Enquiry(models.Model):
    """
    Stores customer enquiries from the contact form.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    message = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the enquiry was submitted."
    )

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Enquiry from {self.name} on {self.created_at.strftime('%Y-%m-%d')}"
