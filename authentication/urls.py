from django.urls import path
from . import views

urlpatterns = [
    path("login",views.Login.as_view(),name="login"),
    path("register",views.Register.as_view(),name="register"),
    path("verifyRequest",views.verifyRequest.as_view(),name="verifyRequest"),
]

htmx_urlpatterns = [
    path('check_id',views.check_id,name="check_id"),
    path('check_email',views.check_email,name="check_email"),
]

urlpatterns +=htmx_urlpatterns