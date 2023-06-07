"""
Tests for Mountain Routes API end-points
"""

import json
import unittest
from datetime import timedelta
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory


AUTHORIZATION_HEADER = 'Token f220ff58293120106dd6925b9cfaa07937e701eb'
RIDGE = 'svidovets'
PEAK = 'bliznitsa'


def test_password_by_username(login):
    suffix = login.split('_')[-1]
    return TEST_PASSWD + suffix


def get_test_user(user=None):
    """
    find first test user
    """
    test_user = get_user_model().objects.filter(
        username=settings.API_TEST_USERNAME).first()
    return test_user if test_user else user


class ApiTestCase(unittest.TestCase):
    """
    Test case to test end-points of Mountain Routes API
    """

    def setUp(self):
        self.client = APIClient()

        self.factory = APIRequestFactory()
        self.user = get_test_user()
        self.climber = self.user.climber

        self.user_token, self.refresh_token = self.get_jwt_token()
        self.set_headers()

    def tearDown(self):
        self.client.logout()

    def set_headers(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer %s' % self.user_token,
            HTTP_ACCEPT_LANGUAGE='ru')

    def get_jwt_token(self, username=None, password=None):
        if username is None and password is None:
            username = self.user.username
            password = settings.API_TEST_PASSWORD or \
                test_password_by_username(self.user.username)
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': username,
                'password': password,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        return r.get('access'), r.get('refresh')

    def test_0000_help(self):
        response = self.client.get(reverse('hello'), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_0002_jwt_tokens(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': self.user.username,
                'password': settings.API_TEST_PASSWORD or
                test_password_by_username(self.user.username),
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)

        self.assertTrue(len(r.get('access')))
        self.assertTrue(len(r.get('refresh')))

        refresh = r.get('refresh')
        response = self.client.post(
            reverse('token_refresh'),
            {
                'refresh': refresh,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        self.assertTrue(len(r.get('access')))

    def test_0010_ridges(self):
        response = self.client.get(reverse('api-ridges'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ridges = json.loads(response.content)

        self.assertTrue(ridges)
        self.assertTrue(isinstance(ridges, list))
        self.assertTrue(len(ridges))
        self.assertTrue(ridges[0]['slug'])

    def test_0020_ridge_by_slug(self):
        response = self.client.get(
            reverse('api-ridge-by-slug', args=[RIDGE]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ridge = json.loads(response.content)
        self.assertTrue(ridge)
        # pprint(ridge)
        self.assertEqual(ridge['slug'], RIDGE)

    # TODO add test ridge with test peaks and test routs
    # field active
    #
    # TODO add end-points ridge with all tree, peak with all tree
