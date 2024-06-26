# Generated by Django 4.1 on 2023-03-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("researchhub_comment", "0008_rhcommentmodel_comment_content_json_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rhcommentthreadmodel",
            name="thread_type",
            field=models.CharField(
                choices=[
                    ("GENERIC_COMMENT", "GENERIC_COMMENT"),
                    ("INNER_CONTENT_COMMENT", "INNER_CONTENT_COMMENT"),
                ],
                default="GENERIC_COMMENT",
                max_length=144,
            ),
        ),
    ]
