"""
views related to application user
"""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from routes.misc import atoi
from .forms import ProfileForm


def user_profile(request):
    """ return user profile """
    return render(
        request, 'User/profile.html', {})


def user_profile_edit(request):
    """ return page to edit user profile """

    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if 'save' in request.POST and form.is_valid():
            data = form.cleaned_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.climber.middle_name = data['middle_name']
            user.climber.save()
            user.save()

            messages.success(request, 'Profile details updated.')
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse('user-profile'))

    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.climber.middle_name,
    }
    form = ProfileForm(initial=data)

    return render(
        request, 'User/profile_edit.html', {'form': form})
