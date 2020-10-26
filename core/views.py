from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Website, Save, SavedWebsites


class HomeView(ListView):
    model = Website
    paginate_by = 10
    template_name = 'core/home.html'


class WebsiteDetailView(DetailView):
    model = Website
    template_name = 'core/website.html'


@login_required
def save_to_profile(request, slug):
    try:
        website = get_object_or_404(Website, slug=slug)
        save_website, created = Save.objects.get_or_create(
            website=website,
            user=request.user,
            saved=False
        )
        saved_qs = SavedWebsites.objects.filter(user=request.user, saved=True)
        if saved_qs.exists():
            savedwebsites = saved_qs[0]
            if savedwebsites.websites.filter(website__slug=website.slug).exists():
                messages.info(request, 'The website is already saved in your profile.')
                return redirect('core:website', slug=slug)
            else:
                save_website.save()
                savedwebsites.websites.add(save_website)
                messages.info(request, 'The website is saved to your profile.')
                return redirect('core:website', slug=slug)
        else:
            savedwebsites = SavedWebsites.objects.create(user=request.user)
            savedwebsites.websites.add(save_website)
            messages.info(request, 'The website is saved to your profile.')
            return redirect('core:website', slug=slug)

    except Exception as e:
        messages.error(request, 'There was an error in saving this website')
        return redirect('core:website', slug=slug)


@login_required
def remove_from_profile(request, slug):
    try:
        website = get_object_or_404(Website, slug=slug)
        saved_qs = SavedWebsites.objects.filter(user=request.user, saved=True)
        if saved_qs.exists():
            savedwebsites = saved_qs[0]
            if savedwebsites.websites.filter(website__slug=website.slug).exists():
                saved_website = Save.objects.filter(
                    website=website,
                    user=request.user,
                    saved=False
                )[0]
                saved_website.save()
                savedwebsites.websites.remove(saved_website)
                messages.info(request, 'The website is removed from your profile.')
                return redirect('account:profile')
            else:
                messages.info(request, 'This website is not saved in your profile.')
                return redirect('account:profile')
        else:
            messages.info(request, 'You do not have anything saved your profile.')
            return redirect('account:profile')

    except Exception as e:
        messages.error(request, 'There was an error in removing this website')
        return redirect('core:home')


def about(request):
    return render(request, 'core/about.html')
