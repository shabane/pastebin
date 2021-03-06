from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('support', views.support),
    path('action/delete', views.delete),
    path('guide', views.guide),
    path('action/share', views.share),
    path('search', views.search),
    path('add', views.add),
    path('<str:link>', views.shared)
]