from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'travelposts/<int:travel_id>/', 
        views.TravelDetailView.as_view(),
        name='travel-detail',
        ),
]