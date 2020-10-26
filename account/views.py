from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from core.models import SavedWebsites


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in now.")
            return redirect('account:login')
        else:
            messages.error(request, "There was an error in creating your. Please try again.")
            return redirect('account:register')
    else:
        form = UserRegistrationForm
        context = {
            'form': form
        }
        return render(request, 'account/register.html', context)


@login_required
def profile(request):
    user = request.user
    websites = SavedWebsites.objects.get(user=request.user, saved=True)
    context = {
        'user': user,
        'websites': websites
    }
    return render(request, 'account/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('account:profile')
        else:
            messages.error(request, "There was an error in updating your profile. Please try again.")
            return redirect('account:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'account/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been changed!")
            return redirect('account:profile')
        else:
            messages.error(request, "There was a problem is changing your password. Please try again.")
            return redirect(reverse('account:profile'))
    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form
        }
        return render(request, 'account/change_password.html', context)
