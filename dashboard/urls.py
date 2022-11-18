from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard.as_view(),name='dashboard'),
    path("Room/Detail/<str:pk>", views.ListingDetail.as_view(),name='ListingDetail'),
    path("Room/Details/<str:pk>", views.AccomodationForm.as_view(),name='AccomodationForm'),
    path("make/Reservation/<str:pk>", views.MakeReservation.as_view(),name='makeReservation'),
    path("CancelReservation/<str:pk>", views.CancelReservation.as_view(),name='CancelReservation'),
    path('serviceRequired',views.serviceRequired.as_view(), name='serviceRequired'),
    path('availableRoom',views.availableRoom.as_view(), name='availableRoom'),
]