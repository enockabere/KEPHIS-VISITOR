from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard.as_view(),name='dashboard'),
    path("Room/Detail/<str:pk>", views.ListingDetail.as_view(),name='ListingDetail'),
    path("make/Reservation/<str:pk>", views.makeReservation,name='makeReservation'),
    path("CancelReservation", views.CancelReservation.as_view(),name='CancelReservation'),
    path('serviceRequired',views.serviceRequired.as_view(), name='serviceRequired'),
    path('availableRoom',views.availableRoom.as_view(), name='availableRoom'),
]