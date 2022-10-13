from django.urls import path
from . import views

urlpatterns = [
    path("login",views.Login.as_view(),name="login"),
    path("register",views.Register.as_view(),name="register"),
    path("verifyRequest",views.verifyRequest.as_view(),name="verifyRequest"),
]