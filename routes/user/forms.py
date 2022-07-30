"""
forms related to app user
"""

import re
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ProfileForm(forms.Form):
    """
    User Profile form
    """
    username = forms.CharField(
        label=_('Username'),
        required=True,
        max_length=16,
        min_length=2,
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
        }),
    )

    first_name = forms.CharField(
        label=_('First name'),
        required=True,
        max_length=32,
        widget=forms.TextInput(attrs={
            'placeholder': _('First name'),
        }),
    )

    middle_name = forms.CharField(
        label=_('Middle name'),
        required=True,
        max_length=32,
        widget=forms.TextInput(attrs={
            'placeholder': _('Middle name'),
        }),
    )

    last_name = forms.CharField(
        label=_('Last name'),
        required=True,
        max_length=32,
        widget=forms.TextInput(attrs={
            'placeholder': _('Last name'),
        }),
    )

    def custom_init(self):
        from fcuser.views import random_username
        username = ''
        for i in range(10):
            username = random_username()
            if not get_user_model().objects.filter(username=username).exists():
                break
        self.fields['username'].initial = username

    #def clean_username(self):
        #username = self.cleaned_data['username']
        #if not re.match(r'^[A-Za-z0-9_\.]{2,16}$', username):
            #raise forms.ValidationError(
                #_("Nickname should be a combination of english alphabets,"
                  #" numbers, underscore and point with length between 2 and 16 symbols"))
        #if username and get_user_model().objects.filter(username__iexact=username).exists():
            #raise ValidationError(_('A user with this nickname already exists'))
        #return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

