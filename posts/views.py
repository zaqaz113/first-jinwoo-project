from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from allauth.account.views import PasswordChangeView

from posts.models import TravelPost

# Create your views here.

class IndexView(ListView):
    model = TravelPost
    template_name = 'posts/index.html'
    context_object_name = 'travelposts'
    paginate_by = 4
    ordering = ["-dt_created"]

class TravelDetailView(DetailView):
    model = TravelPost
    template_name = "posts/travel_detail.html"
    pk_url_kwarg = "travel_id"

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')
