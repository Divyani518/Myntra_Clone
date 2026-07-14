from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone", "address_line1", "address_line2", "city", "state", "pincode")
        widgets = {
            "address_line1": forms.TextInput(attrs={"placeholder": "House / Flat no., Street"}),
            "address_line2": forms.TextInput(attrs={"placeholder": "Area / Locality"}),
        }
