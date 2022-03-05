from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView
from posts.models import User
from posts.models import TravelPost
from posts.forms import TravelForm, ProfileForm
from posts.functions import confirmation_required_redirect


# Create your views here.

class IndexView(ListView):
    model = TravelPost
    template_name = 'posts/index.html'
    context_object_name = 'travelposts'
    paginate_by = 4
    ordering = ["-dt_created"]

class TravelDetailView(DetailView):
    model = TravelPost
    template_name = "posts/travelpost_detail.html"
    pk_url_kwarg = "travel_id"

class TravelCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TravelPost
    form_class = TravelForm
    template_name = "posts/travelpost_form.html"

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('travel-detail', kwargs={"travel_id": self.object.id})

    def test_func(self,user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()



class TravelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TravelPost
    form_class = TravelForm
    template_name = "posts/travelpost_form.html"
    pk_url_kwarg = 'travel_id'

    raise_exception = True

    def get_success_url(self):
        return reverse('travel-detail', kwargs={"travel_id": self.object.id})

    def test_func(self, user):
        travelpost = self.get_object()
        return travelpost.author == user


class TravelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TravelPost
    template_name = 'posts/travelpost_confirm_delete.html'
    pk_url_kwarg = 'travel_id'

    raise_exception = True

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
        travelpost = self.get_object()
        return travelpost.author == user
        

class ProfileView(DetailView):
    model = User
    template_name = 'posts/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_travelposts'] = TravelPost.objects.filter(author__id=user_id).order_by('-dt_created')[:4]
        return context


class UserTravelPostListView(ListView):
    model = TravelPost
    template_name = 'posts/user_travelpost_list.html'
    context_object_name = 'user_travelposts'
    paginate_by = 4

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return TravelPost.objects.filter(author__id=user_id).order_by('-dt_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'posts/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('index')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'posts/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs=({'user_id': self.request.user.id}))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
