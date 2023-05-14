"""
Test case to test models related to mountain routes
"""

import unittest
from .models import GeoPoint, Ridge, thumbnail, slugify_name, PeakComment
from .views import divide_into_groups_of_three


class RouteTestCase(unittest.TestCase):

    def setUp(self):
        self.ridge = Ridge.objects.get(
            slug='svidovets')
        self.peak = self.ridge.peaks().filter(slug='bliznitsa')[0]
        self.route = self.peak.routes()[0]
        self.point = self.peak.point

    def tearDown(self):
        pass

    def test_00_geopoint(self):
        geopoint = GeoPoint.objects.all()[0]
        self.assertTrue(geopoint.latitude)
        self.assertTrue(geopoint.longitude)

    def test_01_ridge(self):
        self.assertTrue(self.ridge.name)
        self.assertTrue(self.ridge.description)

    def test_02_peak(self):
        self.assertTrue(self.peak.name)
        self.assertTrue(self.peak.description)
        self.assertTrue(self.peak.height)

    def test_03_route(self):
        self.assertTrue(self.route.name)

    def test_04_thumbnail(self):
        data = thumbnail(2000, 3000)
        self.assertEqual(data['width'], 266)
        self.assertEqual(data['height'], 400)

    def test_05_slugify_name(self):
        data = slugify_name(Ridge, 'очень высокий холодный хребет')
        self.assertEqual(data, 'ochen-vysokii-kholodnyi-khrebet')

    def test_06_distance_to_point(self):
        apoint = GeoPoint(latitude=0, longitude=0)
        distance = self.point.distance_to_point(apoint)
        self.assertEqual(int(distance), 5847)

    def test_07_distance_to_coordinates(self):
        apoint = GeoPoint(latitude=0, longitude=0)
        distance = self.point.distance_to_coordinates(90, 0)
        self.assertEqual(int(distance), 4645)

    def test_08_degree_from_string(self):
        degree = GeoPoint.degree_from_string('45 37 15')
        self.assertEqual(int(degree * 10000), 456208)

    def test_09_field_value(self):
        data = self.point.field_value()
        self.assertEqual(data, self.point.latitude)

    def test_10_degrees(self):
        self.assertEqual(self.point.degrees('lat'), 48)
        self.assertEqual(self.point.degrees('lon'), 24)

    def test_11_minutes(self):
        self.assertEqual(self.point.minutes('lat'), 13)
        self.assertEqual(self.point.minutes('lon'), 13)

    def test_12_seconds(self):
        self.assertEqual(self.point.seconds('lat'), 18)
        self.assertEqual(self.point.seconds('lon'), 57)

    def test_13_ridge_absolute_url(self):
        self.assertTrue(self.ridge.slug in self.ridge.get_absolute_url())

    def test_14_ridge_peaks(self):
        self.assertTrue(self.ridge.peaks())
        self.assertTrue(self.ridge.routes())

    def test_15_peak_routes(self):
        self.assertTrue(self.peak.routes())

    def test_16_route_data(self):
        self.assertTrue(self.route.number)
        self.assertTrue(self.route.sections)
        self.assertTrue(self.route.points)

    def test_17_divide_list(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8]
        lst1 = divide_into_groups_of_three(lst)
        self.assertEqual(lst1[1], [4, 5, 6])

    def test_18_peak_comments(self):
        self.assertTrue(self.peak.comments())
        
    def test_19_children_comments(self):
        comments = PeakComment.objects.filter(parent__isnull=False, active=True)
        self.assertTrue(comments.count())
        comment = comments[0]
        self.assertTrue(comment.body)
        parent = comment.parent
        self.assertTrue(parent.replies.count())
        
        
if __name__ == '__main__':
    unittest.main()

