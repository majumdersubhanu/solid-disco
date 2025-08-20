from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import Hotel, HotelImage, Destination, DestinationImage, Enquiry

# Unregister the default User and Group models
# admin.site.unregister(User)
admin.site.unregister(Group)


class HotelImageInline(admin.TabularInline):
    """
    Allows adding multiple HotelImage objects from the Hotel admin page.
    Includes a preview of the uploaded image.
    """

    model = HotelImage
    extra = 3  # Show 3 empty forms for uploading images by default
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """
        Creates a thumbnail preview for the image in the admin inline.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url,
            )
        return "(No image)"

    image_preview.short_description = "Image Preview"


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Hotel model.
    """

    inlines = [HotelImageInline]  # Add the inline class here
    list_display = (
        "name",
        "city",
        "country",
        "price_per_night",
        "rating",
        "is_featured",
    )
    list_filter = ("is_featured", "city", "country", "rating")
    search_fields = ("name", "city", "country", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_featured",)
    ordering = ("name",)


class DestinationImageInline(admin.TabularInline):
    """
    Allows adding multiple DestinationImage objects from the Destination admin page.
    Includes a preview of the uploaded image.
    """

    model = DestinationImage
    extra = 3  # Show 3 empty forms for uploading images by default
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """
        Creates a thumbnail preview for the image in the admin inline.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url,
            )
        return "(No image)"

    image_preview.short_description = "Image Preview"


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Destination model.
    """

    inlines = [DestinationImageInline]  # Add the inline class here
    list_display = ("name", "country", "best_time_to_visit", "is_featured")
    list_filter = ("is_featured", "country")
    search_fields = ("name", "country", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_featured",)
    ordering = ("name",)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Enquiry model.
    """

    list_display = (
        "name",
        "email",
        "phone_number",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    # Use a single method for the contact actions
    readonly_fields = (
        "name",
        "email",
        "phone_number",
        "message",
        "created_at",
        "contact_actions",
    )
    ordering = ("-created_at",)

    def contact_actions(self, obj):
        """
        Creates side-by-side buttons for emailing and calling.
        """
        actions = []
        if obj.email:
            email_button_style = "background-color: #417690; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; margin-right: 5px;"
            actions.append(
                format_html(
                    '<a style="{}" href="mailto:{}" target="_blank">Send Email</a>',
                    email_button_style,
                    obj.email,
                )
            )
        if obj.phone_number:
            call_button_style = "background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;"
            actions.append(
                format_html(
                    '<a style="{}" href="tel:{}" target="_blank">Call Now</a>',
                    call_button_style,
                    obj.phone_number,
                )
            )

        if not actions:
            return "No contact info"

        return format_html("".join(actions))

    contact_actions.short_description = "Actions"  # Column header and field label

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


# You can optionally register the image models directly if you want to manage them separately
# admin.site.register(HotelImage)
# admin.site.register(DestinationImage)
