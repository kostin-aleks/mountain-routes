"""
views related to carpathians
"""

import django_filters
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables
from django_tables2.config import RequestConfig

from routes.mountains.models import Ridge, Peak, Route, GeoPoint
from routes.mountains.forms import RidgeForm, PeakForm


class PeakFilter(django_filters.FilterSet):
    """
    Filter Set to filter by peak
    """
    class Meta:
        model = Peak
        fields = []


class PeakTable(tables.Table):
    """
    Table for peaks
    """
    slug = tables.Column(accessor='slug', verbose_name="")
    name = tables.Column(accessor='name', verbose_name="Название")
    height = tables.Column(accessor='height', verbose_name="Высота, м")
    ridge = tables.Column(accessor='ridge__name', verbose_name="Район")

    def render_slug(self, value):
        """render slug"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('peak', args=[value]),
            value)

    def render_ridge(self, value, record):
        """render field ridge"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('ridge', args=[record.ridge.slug]),
            value)

    class Meta:
        attrs = {'class': 'table'}


class RidgeFilter(django_filters.FilterSet):
    """
    Filter Set to filter by ridge
    """
    class Meta:
        model = Ridge
        fields = []


class RidgeTable(tables.Table):
    """
    Table for ridges
    """
    slug = tables.Column(accessor='slug', verbose_name="")
    name = tables.Column(accessor='name', verbose_name="")

    def render_slug(self, value):
        """render field slug"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('ridge', args=[value]),
            value)

    class Meta:
        attrs = {'class': 'table'}


class RouteFilter(django_filters.FilterSet):
    """
    Filter Set to filter by route
    """
    class Meta:
        model = Route
        fields = []


class RouteTable(tables.Table):
    """
    Table for routes
    """
    route_id = tables.Column(accessor='id', verbose_name="route_id")
    number = tables.Column(accessor='number', verbose_name="#")
    name = tables.Column(accessor='name', verbose_name="Название")
    difficulty = tables.Column(accessor='difficulty', verbose_name="КТ")
    peak = tables.Column(accessor='peak__name', verbose_name="Вершина")
    height = tables.Column(accessor='peak__height', verbose_name="Высота")
    author = tables.Column(accessor='author', verbose_name="Автор")
    year = tables.Column(accessor='year', verbose_name="Год")

    def render_route_id(self, value):
        """render field route_id"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('route', args=[value]),
            value)

    def render_peak(self, value, record):
        """render field peak"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('peak', args=[record.peak.slug]),
            value)

    def render_name(self, value, record):
        """render field name"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('route', args=[record.id]),
            value)

    class Meta:
        attrs = {'class': 'table'}


def ridges(request):
    """
    return page with ridges
    """
    user = request.user

    order_by = 'name'
    qs = Ridge.objects.all().order_by(order_by)

    _filter = RidgeFilter(request.GET, queryset=qs)

    ridge_table = RidgeTable(_filter.qs)
    RequestConfig(
        request, paginate={"per_page": 100}).configure(ridge_table)

    return render(
        request,
        'Routes/ridges.html',
        {
            'table': ridge_table,
            'can_edit': user.is_superuser or (user.is_authenticated and user.climber.is_editor),
        })


def ridge(request, slug):
    """
    return page with ridge
    """
    the_ridge = get_object_or_404(Ridge, slug=slug)

    return render(
        request,
        'Routes/ridge.html',
        {
            'ridge': the_ridge,
            'can_be_edited': the_ridge.can_be_edited(request.user),
            'can_be_removed': the_ridge.can_be_removed()})


def peak(request, slug):
    """
    return page for the peak
    """
    the_peak = get_object_or_404(Peak, slug=slug)

    return render(
        request,
        'Routes/peak.html',
        {
            'peak': the_peak,
            'can_be_edited': the_peak.can_be_edited(request.user),
            'can_be_removed': the_peak.can_be_removed()})


def route(request, route_id):
    """
    return page for the route
    """
    the_route = get_object_or_404(Route, pk=route_id)

    return render(
        request,
        'Routes/route.html',
        {'route': the_route})


def routes(request):
    """
    return list of routes
    """
    order_by = 'number'
    qs = Route.objects.all().order_by(order_by)

    _filter = RouteFilter(request.GET, queryset=qs)

    routes_table = RouteTable(_filter.qs)
    RequestConfig(
        request, paginate={"per_page": 100}).configure(routes_table)

    return render(
        request,
        'Routes/routes.html',
        {'table': routes_table})


def peaks(request):
    """
    return list of peaks
    """
    order_by = 'name'
    qs = Peak.objects.all().order_by(order_by)

    _filter = PeakFilter(request.GET, queryset=qs)

    peaks_table = PeakTable(_filter.qs)
    RequestConfig(
        request, paginate={"per_page": 100}).configure(peaks_table)

    return render(
        request,
        'Routes/peaks.html',
        {'table': peaks_table})


@login_required
def add_ridge(request):
    """
    add a new ridge
    """
    user = request.user
    if not (user.is_superuser or user.climber.is_editor):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RidgeForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            ridge = Ridge.objects.create(
                slug=data['slug'],
                name=data['name'],
                description=data['description'])
            return HttpResponseRedirect(reverse('ridges'))
    else:
        form = RidgeForm()

    args = {}
    args['form'] = form

    return render(
        request,
        'Routes/add_ridge.html',
        args)


@login_required
def remove_ridge(request, slug):
    """
    remove the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        data = request.POST
        if 'remove' in data:
            Ridge.objects.filter(slug=data['slug']).delete()
            return HttpResponseRedirect(reverse('ridges'))
        if 'cancel' in data:
            return HttpResponseRedirect(reverse('ridge', args=[the_ridge.slug]))

    args = {'ridge': the_ridge}

    return render(
        request,
        'Routes/remove_ridge.html',
        args)


@login_required
def edit_ridge(request, slug):
    """
    edit the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RidgeForm(request.POST, instance=the_ridge)

        if form.is_valid():
            data = form.cleaned_data
            the_ridge.slug = data['slug']
            the_ridge.name = data['name']
            the_ridge.description = data['description']
            the_ridge.save()

            return HttpResponseRedirect(reverse('ridges'))
    else:
        form = RidgeForm(instance=the_ridge)

    args = {}
    args['form'] = form

    return render(
        request,
        'Routes/edit_ridge.html',
        args)


@login_required
def add_ridge_peak(request, slug):
    """
    edit the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = PeakForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            peak = Peak.objects.create(
                ridge=the_ridge,
                slug=data['slug'],
                name=data['name'],
                description=data['description'],
                height=data['height'],
                point=GeoPoint.objects.create(latitude=data['latitude'], longitude=data['longitude'])
            )
            return HttpResponseRedirect(reverse('ridge', args=[the_ridge.slug]))
    else:
        form = PeakForm()

    args = {'form': form}

    return render(
        request,
        'Routes/add_ridge_peak.html',
        args)


@login_required
def edit_ridge(request, slug):
    """
    edit the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RidgeForm(request.POST, instance=the_ridge)

        if form.is_valid():
            data = form.cleaned_data
            the_ridge.slug = data['slug']
            the_ridge.name = data['name']
            the_ridge.description = data['description']
            the_ridge.save()

            return HttpResponseRedirect(reverse('ridges'))
    else:
        form = RidgeForm(instance=the_ridge)

    args = {}
    args['form'] = form

    return render(
        request,
        'Routes/edit_ridge.html',
        args)


@login_required
def edit_peak(request, slug):
    """
    edit the peak
    """
    user = request.user
    peak = get_object_or_404(Peak, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = PeakForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            peak.slug = data['slug']
            peak.name = data['name']
            peak.description = data['description']
            peak.height = data['height']
            peak.point.latitude = data['latitude']
            peak.point.longitude = data['longitude']
            peak.point.save()
            peak.save()

            return HttpResponseRedirect(reverse('peak', args=[peak.slug]))
    else:
        data = {
            'slug': peak.slug,
            'name': peak.name,
            'description': peak.description,
            'height': peak.height,
            'latitude': peak.point.latitude,
            'longitude': peak.point.longitude,
            'photo': peak.photo
        }
        form = PeakForm(initial=data)

    args = {}
    args['form'] = form

    return render(
        request,
        'Routes/edit_peak.html',
        args)


@login_required
def remove_peak(request, slug):
    """
    remove the peak
    """
    user = request.user
    peak = get_object_or_404(Peak, slug=slug)
    ridge = peak.ridge
    if not (user.is_superuser or (user.climber.is_editor and peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        data = request.POST
        if 'remove' in data:
            Peak.objects.filter(slug=data['slug']).delete()
            return HttpResponseRedirect(reverse('ridge', args=[ridge.slug]))
        if 'cancel' in data:
            return HttpResponseRedirect(reverse('peak', args=[peak.slug]))

    args = {'peak': peak}

    return render(
        request,
        'Routes/remove_peak.html',
        args)


@login_required
def add_peak_route(request, slug):
    """
    add a new route to the peak
    """
    user = request.user
    peak = get_object_or_404(Peak, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            route = Route.objects.create(
                peak=peak,
                slug=data['slug'],
                name=data['name'],
                description=data['description'],
                # height=data['height'],
                # point=GeoPoint.objects.create(latitude=data['latitude'], longitude=data['longitude'])
            )
            return HttpResponseRedirect(reverse('peak', args=[peak.slug]))
    else:
        form = RouteForm()

    args = {'form': form}

    return render(
        request,
        'Routes/add_peak_route.html',
        args)
