# Generated by Django 4.0.8 on 2022-11-11 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0012_person_expire_at_person_expired_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="footertext",
            name="locked",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="locked"
            ),
        ),
        migrations.AddField(
            model_name="footertext",
            name="locked_at",
            field=models.DateTimeField(
                editable=False, null=True, verbose_name="locked at"
            ),
        ),
        migrations.AddField(
            model_name="footertext",
            name="locked_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="locked_%(class)s",
                to=settings.AUTH_USER_MODEL,
                verbose_name="locked by",
            ),
        ),
    ]
