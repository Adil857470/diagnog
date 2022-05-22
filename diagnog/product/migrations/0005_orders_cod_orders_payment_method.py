# Generated by Django 4.0.4 on 2022-05-09 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='cod',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('UPI', 'UPI'), ('NetBanking', 'NetBanking')], max_length=150, null=True),
        ),
    ]