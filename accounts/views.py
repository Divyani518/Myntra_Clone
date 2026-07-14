from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignUpForm, ProfileForm
from .models import Profile
from cart.utils import merge_session_cart


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            merge_session_cart(request)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("home:index")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form, "title": "Sign Up"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            merge_session_cart(request)
            next_url = request.POST.get("next") or "home:index"
            return redirect(next_url)
        messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html", {"title": "Login"})


def logout_view(request):
    logout(request)
    return redirect("home:index")


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(
        request,
        "accounts/profile.html",
        {"form": form, "profile": profile, "title": "My Profile"},
    )
