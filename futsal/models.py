from django.db import models
from django.contrib.auth.models import User, Group
import uuid


class Futsal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    futsal_name = models.CharField(max_length=200)
    futsal_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # Image of the futsal, at least one required.
    futsal_image_1 = models.ImageField(upload_to='images/futsal_images/')
    futsal_image_2 = models.ImageField(
        upload_to='images/futsal_images/', blank=True, null=True)
    futsal_image_3 = models.ImageField(
        upload_to='images/futsal_images/', blank=True, null=True)
    futsal_image_4 = models.ImageField(
        upload_to='images/futsal_images/', blank=True, null=True)
    futsal_image_5 = models.ImageField(
        upload_to='images/futsal_images/', blank=True, null=True)

    # Futsal will need location, google maps link
    location = models.CharField(max_length=400)
    google_maps_link = models.URLField(blank=True, null=True)

    # How many a side?
    a_side = models.CharField(max_length=10)

    # How many grounds?
    grounds = models.IntegerField()

    # Other Facilities
    shower_facility = models.BooleanField(default=False)
    parking_space = models.BooleanField(default=False)
    changing_room = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    # On false display indoor. On True display open ground
    open_ground = models.BooleanField(default=False)

    futsal_description = models.TextField(default="")

    # Date Created and Updated
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    booking_date = models.DateField()
    booking_start_time = models.TimeField()
    booking_end_time = models.TimeField()
    # On false display pending. On True display confirmed
    booking_status = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.futsal.name + ' - ' + self.user.username + ' - ' + str(self.booking_date)
