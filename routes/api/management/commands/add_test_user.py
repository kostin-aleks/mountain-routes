#!/usr/bin/env python
"""
NAME
     add_test_user.py

DESCRIPTION
     Add a test user
     Settings should have 
     API_TEST_USERNAME
     API_TEST_PASSWORD
     API_TEST_EMAIL
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Command """
    help = 'Adds test user'

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(
            username=settings.API_TEST_USERNAME).first()
        if not user:
            user = get_user_model().objects.create_user(
                username=settings.API_TEST_USERNAME,
                password=settings.API_TEST_PASSWORD,
                email=settings.API_TEST_EMAIL
            )

        return f'Test user {user} is ready to test'
