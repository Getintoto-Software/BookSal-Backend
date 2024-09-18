from django.urls.conf import path
from .views import UserProfileCreateView, UserProfileRetrieveView, UserProfileUpdateView, UserProfileDeleteView, UserProfileListView

urlpatterns = [
    path("user/profile/create-user-profile/", UserProfileCreateView.as_view(), name="create-user-profile"), 
    path("user/profile/retrieve-user-profile/<int:user>/", UserProfileRetrieveView.as_view(), name="retrieve-user-profile"),
    path("user/profile/update-user-profile/<int:user>/", UserProfileUpdateView.as_view(), name="update-user-profile"),
    path("user/profile/delete-user-profile/<int:user>/", UserProfileDeleteView.as_view(), name="delete-user-profile"),
    path("user/profile/list-user-profiles/", UserProfileListView.as_view(), name="list-user-profile"),
]