from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import UserRegistrationView, UserLoginView, UserProfileView, HotelViewSet, RoomViewSet, BookingViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('v1/public/user/register/', UserRegistrationView.as_view(), name="register"),
    path('v1/public/user/login/', UserLoginView.as_view(), name="login"),
    path('v1/public/user/profile/', UserProfileView.as_view(), name="profile"),
    path('v1/', include(router.urls)),
]