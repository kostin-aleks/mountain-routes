"""
forms related to app user
"""

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from routes.utils import random_username


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
        """
        custom init
        """
        username = ''
        for i in range(10):
            username = random_username()
            if not get_user_model().objects.filter(username=username).exists():
                break
        self.fields['username'].initial = username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
