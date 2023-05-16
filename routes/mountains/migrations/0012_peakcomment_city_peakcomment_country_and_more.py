# Generated by Django 4.2 on 2023-05-16 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0011_peakcomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='peakcomment',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='peakcomment',
            name='country',
            field=models.CharField(max_length=255, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='peakcomment',
            name='country_code',
            field=models.CharField(max_length=3, null=True, verbose_name='country code'),
        ),
        migrations.AddField(
            model_name='peakcomment',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]