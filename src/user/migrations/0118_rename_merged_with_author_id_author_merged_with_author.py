# Generated by Django 4.2.13 on 2024-07-09 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0117_author_merged_with_author_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="author",
            old_name="merged_with_author_id",
            new_name="merged_with_author",
        ),
    ]
