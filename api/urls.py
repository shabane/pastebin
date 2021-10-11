from django.urls import path
from . import views

urlpatterns = [
    path('addtext', views.AddText),
    path('delete', views.DeleteText),
    path('login', views.UserLogin)
]