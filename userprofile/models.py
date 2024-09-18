from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='images/profile_pictures/', blank=True, null=True)
    
    # Futsal will upload at least 1 image and at most 4 images
    futsal_image_1 = models.ImageField(upload_to='images/futsal_images/')
    futsal_image_2 = models.ImageField(upload_to='images/futsal_images/', blank=True, null=True)
    futsal_image_3 = models.ImageField(upload_to='images/futsal_images/', blank=True, null=True)
    futsal_image_4 = models.ImageField(upload_to='images/futsal_images/', blank=True, null=True)
    
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
    
    # Date Created and Updated
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username