import os
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker

from app.models import (
    Hotel,
    HotelImage,
    Destination,
    DestinationImage,
    Enquiry,
)


class Command(BaseCommand):
    help = "Populates the database with sample data (2 hotels, 5 destinations, 25 enquiries)."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database population...")
        fake = Faker("en_IN")

        # --- Clean up old data ---
        self.stdout.write("Deleting old data...")
        Hotel.objects.all().delete()
        Destination.objects.all().delete()
        Enquiry.objects.all().delete()

        # --- Get Sample Images ---
        sample_images_path = os.path.join(settings.MEDIA_ROOT, "sample_images")
        hotel_images_path = os.path.join(sample_images_path, "hotels")
        dest_images_path = os.path.join(sample_images_path, "destinations")

        try:
            hotel_image_files = [
                f
                for f in os.listdir(hotel_images_path)
                if os.path.isfile(os.path.join(hotel_images_path, f))
            ]
            dest_image_files = [
                f
                for f in os.listdir(dest_images_path)
                if os.path.isfile(os.path.join(dest_images_path, f))
            ]
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "Sample image directories not found. Please create 'media/sample_images/hotels' and 'media/sample_images/destinations' and add images."
                )
            )
            return

        if not hotel_image_files or not dest_image_files:
            self.stdout.write(
                self.style.ERROR(
                    "No images found in sample directories. Please add images to continue."
                )
            )
            return

        # --- Create Hotels (only 2) ---
        self.stdout.write("Creating 2 hotels...")
        amenities_options = [
            "Free Wi-Fi",
            "Swimming Pool",
            "Gym",
            "Parking",
            "Restaurant",
            "Air Conditioning",
            "Pet Friendly",
        ]

        for _ in range(2):
            hotel = Hotel.objects.create(
                name=fake.company() + " Hotel & Suites",
                description=fake.text(max_nb_chars=1500),
                address=fake.street_address(),
                city=fake.city(),
                country=fake.country(),
                price_per_night=round(random.uniform(50.00, 500.00), 2),
                rating=round(random.uniform(3.0, 5.0), 1),
                amenities=", ".join(
                    random.sample(amenities_options, k=random.randint(3, 6))
                ),
                is_featured=random.choice([True, False]),
            )
            # Assign cover image
            random_image_name = random.choice(hotel_image_files)
            image_path = os.path.join(hotel_images_path, random_image_name)
            hotel.image.save(random_image_name, File(open(image_path, "rb")))

            # Create gallery images
            for _ in range(random.randint(3, 6)):
                gallery_image_name = random.choice(hotel_image_files)
                gallery_image_path = os.path.join(hotel_images_path, gallery_image_name)
                hotel_image = HotelImage(hotel=hotel, caption=fake.sentence(nb_words=5))
                hotel_image.image.save(
                    gallery_image_name, File(open(gallery_image_path, "rb"))
                )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Hotel: "{hotel.name}"')
            )

        # --- Create Destinations (only 5) ---
        self.stdout.write("Creating 5 destinations...")
        best_time_options = [
            "October to March",
            "April to June",
            "All Year Round",
            "July to September",
        ]

        for _ in range(5):
            destination = Destination.objects.create(
                name=fake.city(),
                description=fake.text(max_nb_chars=2000),
                country=fake.country(),
                best_time_to_visit=random.choice(best_time_options),
                is_featured=random.choice([True, False]),
            )
            # Assign cover image
            random_image_name = random.choice(dest_image_files)
            image_path = os.path.join(dest_images_path, random_image_name)
            destination.image.save(random_image_name, File(open(image_path, "rb")))

            # Create gallery images
            for _ in range(random.randint(4, 7)):
                gallery_image_name = random.choice(dest_image_files)
                gallery_image_path = os.path.join(dest_images_path, gallery_image_name)
                dest_image = DestinationImage(
                    destination=destination, caption=fake.sentence(nb_words=4)
                )
                dest_image.image.save(
                    gallery_image_name, File(open(gallery_image_path, "rb"))
                )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Destination: "{destination.name}"')
            )

        # --- Create Enquiries (keep 25) ---
        self.stdout.write("Creating 25 enquiries...")
        for _ in range(25):
            Enquiry.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone_number=f"+91{fake.msisdn()[-10:]}",
                message=fake.paragraph(nb_sentences=4),
            )
        self.stdout.write(self.style.SUCCESS("Successfully created 25 enquiries."))

        self.stdout.write(
            self.style.SUCCESS("Database has been successfully populated with 2 hotels, 5 destinations, and 25 enquiries!")
        )
