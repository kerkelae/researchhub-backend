# Generated by Django 4.1 on 2023-10-15 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reputation", "0077_alter_distribution_distribution_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="bounty",
            name="bounty_type",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]