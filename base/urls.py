from django.urls import path
from . import views

urlpatterns = [
    path("profile", views.profileRequest,name='profile'),
    path("contact", views.contact,name='contact'),
    path("faq", views.FAQRequest,name='faq'),
]