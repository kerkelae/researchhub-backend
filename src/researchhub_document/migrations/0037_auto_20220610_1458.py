# Generated by Django 2.2 on 2022-06-10 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub_document', '0036_featuredcontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredcontent',
            name='hub_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='featured_content', to='hub.Hub'),
        ),
    ]
