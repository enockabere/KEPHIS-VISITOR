from django.urls import path
from . import views

urlpatterns = [
    path("Reservation",views.Reservations.as_view(),name="reserve"),
    path("gateway/<str:pk>'",views.BookingGateway.as_view(),name="BookingGateway"),
    path("BookingDetails/<str:pk>'",views.BookingDetails.as_view(),name="BookingDetails"),
]