"""
views related to application user
"""

from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from routes.misc import atoi
from routes.geoname.models import get_city_by_geoname
# from gpsfun.main.GeoMap.models import Location
from routes.user.forms import CityForm
# from gpsfun.geocaching_su_stat.views import get_degree


def user_profile(request):
    """ return user profile """
    return render(
        request,
        'User/profile.html',
        {})


def user_profile_edit(request):
    """ return page to edit user profile """

    def get_form_parameters(city):
        """ return form parameters for the city """
        data = (None, None, None)
        if city:
            data = (city.geonameid, city.admin1, city.country)
        return data

    user = request.user
    user_city = None
    city_id, region, country = get_form_parameters(user_city)
    if user and user.gpsfunuser.geocity:
        user_city = user.gpsfunuser.geocity
        city_id, region, country = get_form_parameters(user_city)

    if request.method == 'POST':
        if 'save' in request.POST:
            city_geoname = atoi(request.POST.get('city'))
            city = get_city_by_geoname(city_geoname)
            if city:
                if user.gpsfunuser.geocity != city:
                    user.gpsfunuser.geocity = city
                    user.gpsfunuser.save()
                    messages.success(request, _('Your city changed'))
                user_city = city
                city_id, region, country = get_form_parameters(user_city)
            else:
                if user_city:
                    user.gpsfunuser.geocity = None
                    user.gpsfunuser.save()
                    messages.warning(request, _('You reset city'))

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.gpsfunuser.middle_name = request.POST.get('middle_name')
            user.gpsfunuser.gcsu_username = request.POST.get('nickname')
            user.gpsfunuser.save()
            user.save()

            messages.success(request, 'Profile details updated.')

    form = CityForm(
        initial={
            'country': country,
            'subject': region,
            'city': city_id,
        },
        user_city=user_city)

    return render(
        request,
        'User/profile_edit.html',
        {
            'form_city': form,
        })
