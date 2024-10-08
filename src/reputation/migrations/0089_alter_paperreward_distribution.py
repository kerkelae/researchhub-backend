# Generated by Django 4.2.14 on 2024-07-26 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "reputation",
            "0088_remove_paperreward_is_paid_paperreward_distribution_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="paperreward",
            name="distribution",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="reputation.distribution",
            ),
        ),
    ]
