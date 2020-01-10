from django.urls import path
from . import views

urlpatterns = [
    path('verify', views.Verify.as_view(), name='Verify')
]