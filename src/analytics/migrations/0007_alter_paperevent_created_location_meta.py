# Generated by Django 4.1 on 2022-11-11 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0006_paperevent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paperevent",
            name="created_location_meta",
            field=models.JSONField(blank=True, null=True),
        ),
    ]