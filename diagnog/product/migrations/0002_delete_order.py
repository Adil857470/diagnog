# Generated by Django 3.0.14 on 2022-06-28 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]