from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django_ckeditor_5.fields import CKEditor5Field


class Futsal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    futsal_name = models.CharField(max_length=200)
    futsal_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    futsal_phone_number = models.BigIntegerField(default=9841111111)
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

    # Base Price Per Hour
    price_per_hour = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    # Descriptive Price table
    price_table = CKEditor5Field(
        'Price Table', config_name='extends', default="")

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

    futsal_description = CKEditor5Field(
        'Futsal Description', config_name='extends')

    # Date Created and Updated
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.futsal_name


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
        return self.user.username + ' - ' + self.futsal.futsal_name + ' - ' + str(self.booking_date)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Matchmaking(models.Model):
    player_1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=f'player_1')
    player_2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=f'player_2', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[(
        'waiting', 'Waiting'), ('matched', 'Matched')], default='waiting', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.player_1) + ' - ' + str(self.player_2)
