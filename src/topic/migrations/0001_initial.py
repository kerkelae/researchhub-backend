# Generated by Django 4.1 on 2024-05-03 20:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("openalex_id", models.CharField(max_length=255, unique=True)),
                ("display_name", models.TextField()),
                ("domain_display_name", models.TextField(blank=True, null=True)),
                (
                    "domain_openalex_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("field_display_name", models.TextField(blank=True, null=True)),
                (
                    "field_openalex_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("subfield_display_name", models.TextField(blank=True, null=True)),
                (
                    "subfield_openalex_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("works_count", models.IntegerField(default=0)),
                ("cited_by_count", models.IntegerField(default=0)),
                (
                    "keywords",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
