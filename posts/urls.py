from django.urls import path
from . import views

urlpatterns = [
    # Post urls
    path('', views.IndexView.as_view(), name='index'),
    path(
        'travelposts/<int:travel_id>/', 
        views.TravelDetailView.as_view(), 
        name='travel-detail',
        ),
    path(
        'travelposts/new/', 
        views.TravelCreateView.as_view(), 
        name='travel-create',
        ),
    path(
        'travelposts/<int:travel_id>/edit/',
        views.TravelUpdateView.as_view(),
        name='travel-update',
    ),
    path(
        'travelposts/<int:travel_id>/delete/',
        views.TravelDeleteView.as_view(),
        name='travel-delete',
    ),

    # Profile urls
    path(
        'users/<int:user_id>/',
        views.ProfileView.as_view(),
        name='profile',
    ),
    path(
        'users/<int:user_id>/travelposts/',
        views.UserTravelPostListView.as_view(),
        name="user-travelpost-list",
    ),
    path(
        'set-profile/',
        views.ProfileSetView.as_view(),
        name='profile-set'
    ),
    path(
        'edit-profile/',
        views.ProfileUpdateView.as_view(),
        name='profile-update'
    )
]