from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard.as_view(),name='dashboard'),
    path("Room/Detail", views.ListingDetail.as_view(),name='ListingDetail'),
    path("CancelReservation", views.CancelReservation.as_view(),name='CancelReservation'),
    path('serviceRequired',views.serviceRequired.as_view(), name='serviceRequired'),
]