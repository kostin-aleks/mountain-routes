# Generated by Django 3.2.13 on 2022-06-20 18:37

from django.db import migrations
from routes.mountains.models import slugify_name


def slugify_title(apps, schema_editor):
    '''
    We can't import the Route model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Route = apps.get_model('mountains', 'Route')
    for route in Route.objects.all():
        if route.name:
            route.slug = slugify_name(Route, route.name)
            route.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0003_auto_20220620_2135'),
    ]

    operations = [
        migrations.RunPython(slugify_title),
    ]
