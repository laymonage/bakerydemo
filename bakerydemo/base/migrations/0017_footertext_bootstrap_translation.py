# Generated by Django 4.0.8 on 2023-01-24 16:13

from django.db import migrations
from wagtail.models import BootstrapTranslatableModel


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0016_footertext_translatable"),
    ]
    # Add one operation for each model to bootstrap here
    # Note: Only include models that are in the same app!
    operations = [
        BootstrapTranslatableModel("base.FooterText"),
    ]
