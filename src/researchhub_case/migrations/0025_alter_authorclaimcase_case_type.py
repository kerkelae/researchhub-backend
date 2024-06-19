# Generated by Django 4.1.13 on 2024-04-23 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("researchhub_case", "0024_delete_externalauthorclaimcase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authorclaimcase",
            name="case_type",
            field=models.CharField(
                choices=[
                    ("AUTHOR_CLAIM", "AUTHOR_CLAIM"),
                    ("PAPER_CLAIM", "PAPER_CLAIM"),
                ],
                max_length=32,
            ),
        ),
    ]