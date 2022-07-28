"""
forms related to mountains
"""

import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from routes.mountains.models import Ridge, Peak, Route


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
    photo = forms.IntegerField(
        label=_('Photo'),
        required=False,
        widget=ImagePreviewWidget())
    latitude = forms.FloatField(
        label=_('Latitude'),
        required=False, )
    longitude = forms.FloatField(
        label=_('Longitude'),
        required=False, )

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(_("The slug must consist only of the characters (a-z, 0-9 and -)."))

        return slug
