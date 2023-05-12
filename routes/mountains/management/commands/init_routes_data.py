#!/usr/bin/env python
"""
NAME
     init_routes_data.py

DESCRIPTION
     Add init data
"""
from os.path import isfile, join as path_join
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from routes.mountains.models import (Ridge, Peak, Route, RouteSection, 
    RoutePoint, GeoPoint)


class Command(BaseCommand):
    """ Command """
    help = 'Adds initial data into database'

    def set_image(self, item, file_name, kind, idx):
        """
        set object image
        """
        dir_path = path_join(settings.STATIC_TEST_DATA, '')
        img_path = path_join(dir_path, file_name)
        f = open(img_path, 'rb')
        item.photo.save(f'{kind}{idx}.jpg', File(f))
        item.save()
        
    def handle(self, *args, **options):
        items = [
            {'slug': 'chernogora', 'name': 'Черногорский хребет'},
            {'slug': 'marmarosh', 'name': 'Мармарошский хребет'},
            {'slug': 'svidovets', 'name': 'Свидовецкий хребет', 
             'description': '''Свидовецкий хребетСвидове́ц (укр. Свидівець) — 
             горный массив в Украинских Карпатах, в Закарпатье. 
             Расположен между реками Тересва (на западе) и Чёрной Тисой (на востоке). '''},
            {'slug': 'gorgany', 'name': 'Горганы'}]
        for item in items:
            ridge = Ridge.objects.get_or_create(slug=item['slug'])[0]
            ridge.name = item['name']
            ridge.description = item.get('description')
            ridge.save()

        items = [
            {'slug': 'bliznitsa', 'name': 'Близница',
                'ridge': 'svidovets', 'height': 1881,
                'description': '''Близни́цы (Ближница) — две горы в восточной части массива Свидовец в Горганах, 
                расположены на территории Карпатского Биосферного Заповедника.

                Располагаются рядом и похожи по форме. Высота высшей (северной) вершины 1883 м. 
                С севера Близницы ограничены горой Драгобрат. 
                Южные и западные склоны пологие, восточные — круто обрываются в сторону расширенного верховья долины
                — ледникового кара с остатками морены и ледниковых озер.''',
                'point': {'lat': '48 13 18', 'lon': '24 13 57'},
                'photo': 'Bliznica.jpg',
                'route': {
                    'name': 'Близница из Восточного цирка',
                    'slug': 'bliznitsa-iz-vostochnogo-tsirka',
                    'number': 1,
                    'photo': 'Bliznica-route.jpg',
                    'short_description': '''
                        Маршрут лавиноопасный. 
                        Посещается очень редко. 
                        Рекомендуется восхождение в малоснежный период''',
                    'description': '''
                        Техническая часть маршрута начинается на полонине Свидовец.
                        Надёжный ориентир - озеро Ивор, расположенное в котле с востока от вершины Близница Северная.
                        На полонину Свидовец можно подняться от горнолыжного курорта Драгобрат снежными полями под крутыми склонами северного гребня в. Близница Северная.
                        Издалека хорошо видно крутые скальные стены Жандармов.
                        Озеро Ивор расположено в котле под Жандармами. От Драгобрата до озера около 2 км''',
                    'recommended_equipment': 'ледорубы, кошки, верёвка.',
                    'max_difficulty': 'II-',
                    'difficulty': '2А',
                    'length': 800,
                    'author': '',
                    'year': 0,
                    'height_difference': 300,
                    'start_height': 1500,
                    'descent': 'Спуск по северному гребню до перемычки перед в. Стог, отсюда по восточному склону в сторону Драгобрата.',
                    'ready': 'Yes',
                    'sections': [
                        {
                            'num': 1,
                            'description': """Подъём на линию восточного ребра от озера Ивор крутым снежным склоном, 
                                крутизна до 30°""",
                            'length': 200,
                            'angle': None,
                            'difficulty': 'I'
                        },
                        {
                            'num': 2,
                            'description': """Подъём по широкому некрутому снежному ребру  
                                под крутой вершинный купол""",
                            'length': 200,
                            'angle': None,
                            'difficulty': 'I-'
                        },
                        {
                            'num': 3,
                            'description': """Подъём на вершину по крутому снежному склону.
                                Крутой взлёт в районе вершины следует обходить справа по крутому снежному кулуару 
                                или немного правее, крутизна 20-45°. Дальше подъём по простому гребню на вершину""",
                            'length': 400,
                            'angle': None,
                            'difficulty': 'I, II-'
                        },
                    ],
                    'points': [
                        {'lat': '48 13 18', 'lon': '24 13 57', 'description': 'озеро Ивор'},
                        {'lat': '48 13 18', 'lon': '24 13 57', 'description': 'вершина Близница'},
                    ]
                },
            },
            {'slug': 'brebeneskul', 'name': 'Бребенескул',
                'ridge': 'chernogora', 'height': 2035,
                'point': {'lat': '48 05 54', 'lon': '24 34 50'}},
            {'slug': 'breskul', 'name': 'Брескул',
                'ridge': 'chernogora', 'height': 1911,
                'point': {'lat': '48 09 01', 'lon': '24 30 42'}},
            {'slug': 'hoverla', 'name': 'Говерла',
                'ridge': 'chernogora', 'height': 2061,
                'point': {'lat': '48 09 36', 'lon': '24 30 00'}},
            {'slug': 'hutyn-tomnatyk', 'name': 'Гутин Томнатик',
                'ridge': 'chernogora', 'height': 2016,
                'point': {'lat': '48 05 59', 'lon': '24 33 24'}},
            {'slug': 'igrovets', 'name': 'Игровец',
                'ridge': 'gorgany', 'height': 1814,
                'point': {'lat': '48 35 52', 'lon': '24 05 58'}},
            {'slug': 'syvulja', 'name': 'Сивуля',
                'ridge': 'gorgany', 'height': 1836,
                'point': {'lat': '48 32 57', 'lon': '24 07 12'}},
            {'slug': 'petros', 'name': 'Петрос',
                'ridge': 'chernogora', 'height': 2020,
                'point': {'lat': '48 10 19', 'lon': '24 25 16'}},
            {'slug': 'petrosul', 'name': 'Петросул',
                'ridge': 'chernogora', 'height': 1855,
                'point': {'lat': '48 10 50', 'lon': '24 25 04'}},
            {'slug': 'sheshul', 'name': 'Шешул',
                'ridge': 'chernogora', 'height': 1726,
                'point': {'lat': '48 09 01', 'lon': '24 22 00'}},
            {'slug': 'pozhezhevska', 'name': 'Пожижевская',
                'ridge': 'chernogora', 'height': 1822,
                'point': {'lat': '48 08 40', 'lon': '24 31 25'}},
            {'slug': 'pop-ivan', 'name': 'Поп Иван',
                'ridge': 'chernogora', 'height': 2020,
                'point': {'lat': '48 02 50', 'lon': '24 37 40'}},
            {'slug': 'pop-ivan-marmarosh', 'name': 'Поп Иван Мармарошский',
                'ridge': 'marmarosh', 'height': 1937,
                'point': {'lat': '47 55 26', 'lon': '24 19 41'}},
            {'slug': 'sherban', 'name': 'Шербан',
                'ridge': 'marmarosh', 'height': 1793,
                'point': {'lat': '47 54 419', 'lon': '24 25 16'}},
            {'slug': 'rebra', 'name': 'Ребра',
                'ridge': 'chernogora', 'height': 2001,
                'point': {'lat': '48 06 40', 'lon': '24 33 32'}},
            {'slug': 'turkul', 'name': 'Туркул',
                'ridge': 'chernogora', 'height': 1933,
                'point': {'lat': '48 07 25', 'lon': '24 31 50'}},
            {'slug': 'dantsyzh', 'name': 'Данциж',
                'ridge': 'chernogora', 'height': 1850,
                'point': {'lat': '48 08 08', 'lon': '24 31 54'}},
            {'slug': 'shpytsi', 'name': 'Шпицы',
                'ridge': 'chernogora', 'height': 1863,
                'point': {'lat': '48 07 33', 'lon': '24 34 03'}},
            {'slug': 'rypa', 'name': 'Рыпа',
                'ridge': 'marmarosh', 'height': 1872,
                'point': {'lat': '47 55 06', 'lon': '24 20 19'}},
        ]
        for item in items:
            ridge = Ridge.objects.get(slug=item['ridge'])
            peak = Peak.objects.get_or_create(
                slug=item['slug'], ridge=ridge)[0]
            peak.name = item['name']
            peak.height = item['height']
            peak.description = item.get('description')
            peak.point = GeoPoint.objects.create(
                latitude=GeoPoint.degree_from_string(item['point']['lat']),
                longitude=GeoPoint.degree_from_string(item['point']['lon']),
            )
            peak.save()
            
            # inage
            if 'photo' in item:
                self.set_image(peak, item['photo'], 'peak', 'rst')
            
            if 'route' in item:
                route_item = item['route']
                route = Route.objects.get_or_create(
                    peak=peak,
                    slug=route_item.get('slug')
                )[0]
                route.name=route_item.get('name')
                route.number=route_item.get('number')
                route.description=route_item.get('description')
                route.short_description=route_item.get('short_description')
                route.recommended_equipment=route_item.get('recommended_equipment')
                route.difficulty=route_item.get('difficulty')
                route.max_difficulty=route_item.get('max_difficulty')
                route.length=route_item.get('length') or None
                route.author=route_item.get('author') or ''
                route.year=route_item.get('year') or None
                route.height_difference=route_item.get('height_difference') or None
                route.start_height=route_item.get('start_height') or None
                route.descent=route_item.get('descent') or ''
                route.editor=None
                route.ready=True if route_item.get('ready') else False

                route.save()
                
                # inage
                if 'photo' in route_item:
                    self.set_image(route, item['photo'], 'route', 'rst')
                
                if 'sections' in route_item:
                    for section_item in route_item['sections']:
                        section = RouteSection.objects.get_or_create(
                            route=route,
                            num=section_item['num']
                        )[0]
                        section.save()
                        
                        section.description = section_item.get('description') or ''
                        section.length = section_item.get('length')
                        section.angle = section_item.get('angle')
                        section.difficulty = section_item.get('difficulty') or ''
                        section.save()
                        
                if 'points' in route_item:
                    route.points.delete()
                    for point_item in route_item['points']:
                        point = GeoPoint.objects.create(
                            latitude=GeoPoint.degree_from_string(point_item['lat']),
                            longitude=GeoPoint.degree_from_string(point_item['lon']))
                        route_point = RoutePoint.objects.create(
                            route=route,
                            point=point,
                            description=point_item['description']
                        )

        return 'Initial data is updated'

