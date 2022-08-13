"""
Test case to test models related to mountain routes
"""

import unittest
from .models import GeoPoint, Ridge


class RouteTestCase(unittest.TestCase):

    def setUp(self):
        pass
        self.ridge = Ridge.objects.get(
            slug='chernogora')
        self.peak = self.ridge.peaks().filter(slug='hutyn-tomnatyk')[0]
        self.route = self.peak.routes()[0]

    def tearDown(self):
        pass

    def test_00_geopoint(self):
        geopoint = GeoPoint.objects.all()[0]
        self.assertTrue(geopoint.latitude)
        self.assertTrue(geopoint.longitude)

    def test_01_ridge(self):
        self.assertTrue(self.ridge.name)

    def test_02_peak(self):
        self.assertTrue(self.peak.name)

    def test_03_route(self):
        self.assertTrue(self.route.name)


if __name__ == '__main__':
    unittest.main()

