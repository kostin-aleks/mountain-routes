# Generated by Django 4.2 on 2023-05-12 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mountains', '0005_route_recommended_equipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeakComment',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=80, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('author', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.PROTECT,
                    to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('peak', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments', to='mountains.peak')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
