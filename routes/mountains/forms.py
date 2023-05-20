"""
forms related to mountains
"""

from lxml import etree
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from bs4 import BeautifulSoup
from captcha.fields import CaptchaField

from routes.mountains.models import Ridge, RouteSection
from routes.utils import ridges_list, peaks_list, ANY


class ImagePreviewWidget(forms.widgets.FileInput):
    """
    Widget ImagePreview
    """

    def render(self, name, value, attrs=None, **kwargs):
        """
        render
        """
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
        """
        validate field slug
        """
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(
                _("The slug must consist only of the characters (a-z, 0-9 and -)."))

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


class NewPeakForm(forms.Form):
    """ Form for new Peak """
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
    latitude = forms.CharField(
        label=_('Latitude'),
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Latitude DD MM SS'),
        }), )
    longitude = forms.CharField(
        label=_('Longitude'),
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Longitude DD MM SS'),
        }), )

    def clean_slug(self):
        """
        validate field slug
        """
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(
                _("The slug must consist only of the characters (a-z, 0-9 and -)."))

        return slug


class PeakForm(NewPeakForm):
    """ Form for Peak """
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
    latitude = forms.CharField(
        required=False, )
    longitude = forms.CharField(
        required=False, )


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
        """
        validate field slug
        """
        slug = self.cleaned_data['slug']
        pattern = r'[^\-a-z0-9]'
        if re.search(pattern, slug):
            # Character other then . a-z 0-9 was found
            raise ValidationError(
                _("The slug must consist only of the characters (a-z, 0-9 and -)."))

        return slug


class PeakUserCommentForm(forms.Form):
    """ Form for New User Comment """
    body = forms.CharField(
        label=_('Body'),
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': _('New comment'),
                'rows': 5, 'cols': 50,
            }), )

    photo = forms.ImageField(
        label=_('Photo'),
        required=False,
        widget=ImagePreviewWidget())

    doc = forms.FileField(
        label=_('Text'),
        required=False,
    )

    def clean_body(self):
        """
        Avoid using restricted tags in comment body
        """
        ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
        txt = self.cleaned_data.get('body')

        tags = re.search("<[^>]*>", txt)
        if not tags:
            return txt

        tags = re.findall("<[^>]*>", txt)
        for item in tags:
            tag = re.search("<[\s,\/]*([a-z,A-Z]+)\s*[^>]*>", item)
            tag_name = tag.groups()[0]

            if tag_name not in ALLOWED_TAGS:
                raise ValidationError(
                    _("You use prohibited tags. You can use only tags <i>, <code>, <strong> and <a>."))

        parser = etree.XMLParser()
        try:
            tree = etree.XML(f'<html>{txt}</html>', parser)
        except etree.XMLSyntaxError:
            raise ValidationError(
                _("Fix syntax errors in html tags."))

        soup = BeautifulSoup(txt, 'lxml')
        while True:
            replaced = False
            for tag in soup.descendants:
                if tag.name and tag.name not in ALLOWED_TAGS:
                    tag.unwrap()
                    replaced = True
            if replaced:
                break

        if False:
            raise ValidationError(
                _("You use prohibited tags. You can use only tags <i>, <code>, <strong> and <a>."))

        return str(soup)


class PeakCommentForm(PeakUserCommentForm):
    """ Form for New Comment for Anonimous """

    name = forms.CharField(
        label=_('User name*'),
        required=True,
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('User name'),
            }), )

    email = forms.EmailField(
        label=_('Email*'),
        required=True,
        widget=forms.TextInput(),
        initial='someuser@some.server.com'
    )

    homepage = forms.URLField(
        label=_('Home page'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Home page'),
            })
    )

    captcha = CaptchaField(required=True)

    def clean_name(self):
        """
        validate field name
        """
        name = self.cleaned_data['name']
        pattern = r'[^a-zA-Z0-9]'
        if re.search(pattern, name):
            # Character other then a-z A-Z 0-9 was found
            raise ValidationError(
                _("The user name must consist only of the characters (a-z, A-Z, 0-9)."))

        return name


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


class RouteNewPointForm(forms.Form):
    """ Form for new RoutePoint """
    latitude = forms.CharField(
        label=_('Latitude'),
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Latitude DD MM SS'),
        }), )

    longitude = forms.CharField(
        label=_('Longitude'),
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Longitude DD MM SS'),
        }), )

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
            'rows': 2,
        }), )


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


class FilterPeaksForm(forms.Form):
    """
    Form to filter list of peaks
    """

    ridge = forms.ChoiceField(
        required=False,
        initial='', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        items = ridges_list()
        items[0] = (ANY, _('--any--'))
        self.fields['ridge'] = forms.ChoiceField(
            choices=items,
            required=False,
            initial='',
            widget=forms.Select(attrs={
                'class': '',
                'hx-indicator': '.htmx-indicator',
                'onchange': 'this.form.submit()'
            })
        )


class FilterRoutesForm(forms.Form):
    """
    Form to filter list of routes
    """

    peak = forms.ChoiceField(
        required=False,
        initial='', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        items = peaks_list()
        items[0] = (ANY, _('--any--'))
        self.fields['peak'] = forms.ChoiceField(
            choices=items,
            required=False,
            initial='',
            widget=forms.Select(attrs={
                'class': '',
                'hx-indicator': '.htmx-indicator',
                'onchange': 'this.form.submit()'
            })
        )
