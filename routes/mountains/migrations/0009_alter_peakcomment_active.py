# Generated by Django 4.2 on 2023-05-12 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0008_peakcomment_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peakcomment',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]