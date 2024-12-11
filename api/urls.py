from django.urls.conf import path
from .views import UserProfileCreateAPIView, UserProfileRetrieveAPIView, UserProfileUpdateAPIView, UserProfileDeleteAPIView, UserProfileListAPIView
from .views import FutsalListAPIView, FutsalCreateAPIView, FutsalRetrieveAPIView, FutsalUpdateAPIView, FutsalDeleteAPIView
from .views import BookingListAPIView, BookingCreateAPIView, BookingRetrieveAPIView, BookingUpdateAPIView, BookingDeleteAPIView


urlpatterns = [
    path("user/profile/create-user-profile/",
         UserProfileCreateAPIView.as_view(), name="create-user-profile"),
    path("user/profile/retrieve-user-profile/<int:user>/",
         UserProfileRetrieveAPIView.as_view(), name="retrieve-user-profile"),
    path("user/profile/update-user-profile/<int:user>/",
         UserProfileUpdateAPIView.as_view(), name="update-user-profile"),
    path("user/profile/delete-user-profile/<int:user>/",
         UserProfileDeleteAPIView.as_view(), name="delete-user-profile"),
    path("user/profile/list-user-profiles/",
         UserProfileListAPIView.as_view(), name="list-user-profile"),

    path("futsal/list-futsals/", FutsalListAPIView.as_view(), name="list-futsals"),
    path("futsal/create-futsal/",
         FutsalCreateAPIView.as_view(), name="create-futsal"),
    path("futsal/retrieve-futsal/<int:pk>/",
         FutsalRetrieveAPIView.as_view(), name="retrieve-futsal"),
    path("futsal/update-futsal/<int:pk>/",
         FutsalUpdateAPIView.as_view(), name="update-futsal"),
    path("futsal/delete-futsal/<int:pk>/",
         FutsalDeleteAPIView.as_view(), name="delete-futsal"),

    path("booking/list-bookings/",
         BookingListAPIView.as_view(), name="list-bookings"),
    path("booking/create-booking/",
         BookingCreateAPIView.as_view(), name="create-booking"),
    path("booking/retrieve-booking/<int:pk>/",
         BookingRetrieveAPIView.as_view(), name="retrieve-booking"),
    path("booking/update-booking/<int:pk>/",
         BookingUpdateAPIView.as_view(), name="update-booking"),
    path("booking/delete-booking/<int:pk>/",
         BookingDeleteAPIView.as_view(), name="delete-booking"),

]
