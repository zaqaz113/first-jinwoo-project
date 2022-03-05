from django import forms
from .models import TravelPost, User

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["nickname"]

#     def signup(self, request, user):
#         user.nickname = self.cleaned_data["nickname"]
#         user.save()

class TravelForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        fields = [
            "title",
            "travel_name",
            "travel_link",
            "rating",
            "image1",
            "image2",
            "image3",
            "content",
        ]
        widgets = {
            "rating": forms.RadioSelect,
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname',
            'profile_pic',
            'intro',
        ]
        widget = {
            'intro': forms.Textarea
        }