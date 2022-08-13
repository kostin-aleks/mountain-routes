"""
forms related to mountains
"""

import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from routes.mountains.models import Ridge, Peak, Route, RouteSection


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            img_html = mark_safe(
                f'<br><br><img src="{value.url}" width="100" height="100" />')
        else:
            img_html = ''
        return f'{input_html}{img_html}'


class RidgeForm(forms.ModelForm):
    """ Form for Ridge """
    class Meta:
        model = Ridge
        fields = (
            'name',
            'slug',
            'description',
        )

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(_("The slug must consist only of the characters (a-z, 0-9 and -)."))

        return slug


class PeakPhotoForm(forms.Form):
    """ Form for Peak Photo """
    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
        }), )

    photo = forms.ImageField(
        label=_('Photo'),
        required=False,
        widget=ImagePreviewWidget())


class PeakForm(forms.Form):
    """ Form for Peak """
    name = forms.CharField(
        label=_('Name'),
        required=True,
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': _('Name of summit'),
        }), )
    slug = forms.CharField(
        label=_('Slug'),
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': _('Slug'),
        }), )
    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
        }), )
    height = forms.IntegerField(
        label=_('Height'),
        required=False, )
    photo = forms.ImageField(
        label=_('Photo'),
        required=False,
        widget=ImagePreviewWidget())
    latitude_degree = forms.IntegerField(
        label=_('degrees'),
        required=True,
        min_value=-180,
        max_value=180,
        widget=forms.NumberInput(attrs={'size': 4})
    )
    latitude_minute = forms.IntegerField(
        label=_('minutes'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )
    latitude_second = forms.IntegerField(
        label=_('seconds'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )

    longitude_degree = forms.IntegerField(
        label=_('degrees'),
        required=True,
        min_value=-180,
        max_value=180,
        widget=forms.NumberInput(attrs={'size': 4})
    )
    longitude_minute = forms.IntegerField(
        label=_('minutes'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )
    longitude_second = forms.IntegerField(
        label=_('seconds'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(_("The slug must consist only of the characters (a-z, 0-9 and -)."))

        return slug


class RouteForm(forms.Form):
    """ Form for Route """
    name = forms.CharField(
        label=_('Name'),
        required=True,
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': _('Name of route'),
        }), )
    slug = forms.CharField(
        label=_('Slug'),
        required=False,
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': _('Slug'),
        }), )
    number = forms.IntegerField(
        label=_('Number'),
        required=False, )
    short_description = forms.CharField(
        label=_('Short Description'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Short description'),
        }), )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
        }), )
    recommended_equipment = forms.CharField(
        label=_('Recommended Equipment'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Recommended equipment'),
        }), )
    difficulty = forms.CharField(
        label=_('Difficulty'),
        required=False,
        max_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': _('Difficulty'),
        }), )
    max_difficulty = forms.CharField(
        label=_('Maximal Difficulty'),
        required=False,
        max_length=16,
        widget=forms.TextInput(attrs={
            'placeholder': _('Maximal difficulty'),
        }), )
    length = forms.IntegerField(
        label=_('Length'),
        required=False, )
    photo = forms.ImageField(
        label=_('Photo'),
        required=False,
        widget=ImagePreviewWidget())
    map_image = forms.ImageField(
        label=_('Map'),
        required=False,
        widget=ImagePreviewWidget())
    author = forms.CharField(
        label=_('Author'),
        required=False,
        max_length=64,
        widget=forms.TextInput(attrs={
            'placeholder': _('Author'),
        }), )
    year = forms.IntegerField(
        label=_('Year'),
        required=False, )
    height_difference = forms.IntegerField(
        label=_('Height Difference'),
        required=False, )
    start_height = forms.IntegerField(
        label=_('Start Height'),
        required=False, )
    descent = forms.CharField(
        label=_('Descent'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Descent'),
        }), )
    ready = forms.BooleanField(
        label=_('Ready'),
        required=False, )

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(_("The slug must consist only of the characters (a-z, 0-9 and -)."))

        return slug


class RouteSectionForm(forms.ModelForm):
    """ Form for RouteSection """
    class Meta:
        model = RouteSection
        fields = (
            'num',
            'description',
            'length',
            'angle',
            'difficulty',
        )


class RoutePointForm(forms.Form):
    """ Form for RoutePoint """
    latitude_degree = forms.IntegerField(
        label=_('degrees'),
        required=True,
        min_value=-180,
        max_value=180,
        widget=forms.NumberInput(attrs={'size': 4})
    )
    latitude_minute = forms.IntegerField(
        label=_('minutes'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )
    latitude_second = forms.IntegerField(
        label=_('seconds'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )

    longitude_degree = forms.IntegerField(
        label=_('degrees'),
        required=True,
        min_value=-180,
        max_value=180,
        widget=forms.NumberInput(attrs={'size': 4})
    )
    longitude_minute = forms.IntegerField(
        label=_('minutes'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )
    longitude_second = forms.IntegerField(
        label=_('seconds'),
        required=True,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(attrs={'size': 2})
    )

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
            'rows': 2,
        }), )


class RoutePhotoForm(forms.Form):
    """ Form for Route Photo """
    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
        }), )

    photo = forms.ImageField(
        label=_('Photo'),
        required=False,
        widget=ImagePreviewWidget())


class RidgeLinkForm(forms.Form):
    """ Form for RidgeLink """
    link = forms.URLField(
        label=_('Link'),
        required=True,
        min_length=5,
        widget=forms.URLInput(attrs={'size': 40})
    )

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
            'rows': 2,
            'cols': 40,
        }), )
