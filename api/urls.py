from django.urls.conf import path
from .views import UserProfileCreateView

urlpatterns = [
    path("create-user-profile/", UserProfileCreateView.as_view(), name="create-user-profile"), 
    
]