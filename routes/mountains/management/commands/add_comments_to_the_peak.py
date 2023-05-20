#!/usr/bin/env python
"""
NAME
     add_comments_to_the_peak.py

DESCRIPTION
     Add some comments to the peak
"""

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from routes.mountains.models import Peak, PeakComment


class Command(BaseCommand):
    """ Command """
    help = 'Adds fake comments to the peak'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--peak', help='Peak slug', required=True)

    def handle(self, *args, **options):
        peak = get_object_or_404(Peak, slug=options['peak'])
        NUM = 20
        PeakComment.add_test_comments(peak, count=NUM)

        return f'{NUM} comments are added to the peak {peak.name}'
