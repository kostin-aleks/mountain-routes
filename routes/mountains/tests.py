"""
Test case to test models related to mountain routes
"""

import unittest
from .models import GeoPoint, Ridge, thumbnail, slugify_name, PeakComment
from .views import divide_into_groups_of_three


class RouteTestCase(unittest.TestCase):
    """
    Test case for classes in mountains
    """

    def setUp(self):
        """ setUp """
        self.ridge = Ridge.objects.get(
            slug='svidovets')
        self.peak = self.ridge.peaks().filter(slug='bliznitsa')[0]
        self.route = self.peak.routes()[0]
        self.point = self.peak.point

    def tearDown(self):
        """ tearDown """
        pass

    def test_00_geopoint(self):
        """ test geopoint """
        geopoint = GeoPoint.objects.all()[0]
        self.assertTrue(geopoint.latitude)
        self.assertTrue(geopoint.longitude)

    def test_01_ridge(self):
        """ test ridge """
        self.assertTrue(self.ridge.name)
        self.assertTrue(self.ridge.description)

    def test_02_peak(self):
        """ test peak """
        self.assertTrue(self.peak.name)
        self.assertTrue(self.peak.description)
        self.assertTrue(self.peak.height)

    def test_03_route(self):
        """ test route """
        self.assertTrue(self.route.name)

    def test_04_thumbnail(self):
        """ test thumbnail """
        data = thumbnail(2000, 3000)
        self.assertEqual(data['width'], 266)
        self.assertEqual(data['height'], 400)

    def test_05_slugify_name(self):
        """ test function slugify_name """
        data = slugify_name(Ridge, 'очень высокий холодный хребет')
        self.assertEqual(data, 'ochen-vysokii-kholodnyi-khrebet')

    def test_06_distance_to_point(self):
        """ test GeoPoint.distance_to_point """
        apoint = GeoPoint(latitude=0, longitude=0)
        distance = self.point.distance_to_point(apoint)
        self.assertEqual(int(distance), 5847)

    def test_07_distance_to_coordinates(self):
        """ test GeoPoint.distance_to_coordinates """
        # apoint = GeoPoint(latitude=0, longitude=0)
        distance = self.point.distance_to_coordinates(90, 0)
        self.assertEqual(int(distance), 4645)

    def test_08_degree_from_string(self):
        """ test GeoPoint.degree_from_string """
        degree = GeoPoint.degree_from_string('45 37 15')
        self.assertEqual(int(degree * 10000), 456208)

    def test_09_field_value(self):
        """ test GeoPoint.field_value """
        data = self.point.field_value()
        self.assertEqual(data, self.point.latitude)

    def test_10_degrees(self):
        """ test GeoPoint.degrees """
        self.assertEqual(self.point.degrees('lat'), 48)
        self.assertEqual(self.point.degrees('lon'), 24)

    def test_11_minutes(self):
        """ test GeoPoint.minutes """
        self.assertEqual(self.point.minutes('lat'), 13)
        self.assertEqual(self.point.minutes('lon'), 13)

    def test_12_seconds(self):
        """ test GeoPoint.seconds """
        self.assertEqual(self.point.seconds('lat'), 18)
        self.assertEqual(self.point.seconds('lon'), 57)

    def test_13_ridge_absolute_url(self):
        """ test Ridge.absolute_url """
        self.assertTrue(self.ridge.slug in self.ridge.get_absolute_url())

    def test_14_ridge_peaks(self):
        """ test Ridge.peaks """
        self.assertTrue(self.ridge.peaks())
        self.assertTrue(self.ridge.routes())

    def test_15_peak_routes(self):
        """ test Ridge.routes """
        self.assertTrue(self.peak.routes())

    def test_16_route_data(self):
        """ test Route data """
        self.assertTrue(self.route.number)
        self.assertTrue(self.route.sections)
        self.assertTrue(self.route.points)

    def test_17_divide_list(self):
        """ test function divide_into_groups_of_three """
        lst = [1, 2, 3, 4, 5, 6, 7, 8]
        lst1 = divide_into_groups_of_three(lst)
        self.assertEqual(lst1[1], [4, 5, 6])

    def test_18_peak_comments(self):
        """ test Peak comments """
        self.assertTrue(self.peak.comments())

    def test_19_children_comments(self):
        """ test PeakComment children comments """
        comments = PeakComment.objects.filter(parent__isnull=False, active=True)
        self.assertTrue(comments.count())
        comment = comments[0]
        self.assertTrue(comment.body)
        parent = comment.parent
        self.assertTrue(parent.replies.count())


if __name__ == '__main__':
    unittest.main()
