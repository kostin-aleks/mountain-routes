# Generated by Django 4.2 on 2023-05-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0013_alter_peakcomment_country_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='peakcomment',
            name='region',
            field=models.CharField(max_length=255, null=True, verbose_name='region'),
        ),
    ]
