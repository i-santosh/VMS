# Generated by Django 5.0.4 on 2024-05-04 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('contact_details', models.TextField()),
                ('address', models.TextField()),
                ('vendor_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('on_time_delivery_rate', models.FloatField(blank=True, default=0.0)),
                ('quality_rating_avg', models.FloatField(blank=True, default=0.0)),
                ('average_response_time', models.FloatField(blank=True, default=0.0)),
                ('fulfillment_rate', models.FloatField(blank=True, default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('on_time_delivery_rate', models.FloatField(blank=True, null=True)),
                ('quality_rating_avg', models.FloatField(blank=True, null=True)),
                ('average_response_time', models.FloatField(blank=True, null=True)),
                ('fulfillment_rate', models.FloatField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
        ),
    ]
