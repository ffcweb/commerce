# Generated by Django 4.2.7 on 2023-11-13 11:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_listing_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="image",
        ),
    ]
