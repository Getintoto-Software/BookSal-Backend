from django.db import models
from django.contrib.auth.models import User, Group
import uuid
    
    
class Booking(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    futsal = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_name = models.CharField(max_length=200)
    phone_number = models.BigIntegerField()
    booking_date = models.DateField()
    booking_start_time = models.TimeField()
    booking_end_time = models.TimeField()
    booking_status = models.BooleanField(default=False)
    
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.futsal.name + ' - ' + self.user.username + ' - ' + str(self.date)