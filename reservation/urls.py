from django.urls import path
from . import views

urlpatterns = [
    path("Reservation",views.Reservations.as_view(),name="reserve"),
    path("gateway/<str:pk>",views.BookingGateway.as_view(),name="BookingGateway"),
    path("BookingDetails/<str:pk>",views.BookingDetails.as_view(),name="BookingDetails"),
    path("BookingDetails/<str:pk>",views.BookingDetails.as_view(),name="BookingDetails"),
    path("MeetingDetails/<str:pk>",views.MeetingDetails.as_view(),name="MeetingDetails"),
    path("AccomodationDetails/<str:pk>",views.AccomodationDetails.as_view(),name="AccomodationDetails"),
    path("Pay/<str:pk>",views.Pay.as_view(),name="Pay"),
    path("Confirm/<str:pk>",views.Confirm.as_view(),name="Confirm"),
]