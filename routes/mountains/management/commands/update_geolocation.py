#!/usr/bin/env python
"""
NAME
     update_geolocation.py

DESCRIPTION
     Update geolocation of the user comments
"""

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from routes.mountains.models import PeakComment
from routes.utils import ip_geolocation


class Command(BaseCommand):
    """ Command """
    help = 'Update geolocation of the user comments'
   
    def handle(self, *args, **options):
        cnt = 0
        for comment in PeakComment.objects.filter(
            ip_address__isnull=False, country_code__isnull=True):
            
            try:
                geolocation = ip_geolocation(comment.ip_address)
                comment.country_code = geolocation.get('country_code')
                comment.country = geolocation.get('country')
                comment.city = geolocation.get('city')
                comment.save()  
                cnt += 1
            except ConnectionError as e:
                print("Connection aborted.")
                break
        
        return f'{cnt} comments are updated with geolocation data'
