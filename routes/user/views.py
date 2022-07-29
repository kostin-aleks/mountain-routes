"""
views related to application user
"""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from routes.misc import atoi


def user_profile(request):
    """ return user profile """
    return render(
        request,
        'User/profile.html',
        {})


def user_profile_edit(request):
    """ return page to edit user profile """

    user = request.user

    if request.method == 'POST':
        if 'save' in request.POST:
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.climber.middle_name = request.POST.get('middle_name')
            user.climber.save()
            user.save()

            messages.success(request, 'Profile details updated.')
        return HttpResponseRedirect(reverse('user-profile'))


    return render(
        request, 'User/profile_edit.html', {})
