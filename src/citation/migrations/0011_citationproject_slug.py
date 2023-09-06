# Generated by Django 4.1 on 2023-08-23 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("citation", "0010_remove_citationentry_unified_doc_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="citationproject",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Slug is automatically generated on a signal, so it is not needed in a form",
                max_length=1024,
            ),
        ),
    ]