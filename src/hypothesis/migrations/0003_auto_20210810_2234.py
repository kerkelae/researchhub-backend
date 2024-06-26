# Generated by Django 2.2 on 2021-08-10 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hypothesis', '0002_auto_20210805_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='hypothesis',
            name='renderable_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='hypothesis',
            name='src',
            field=models.FileField(blank=True, default=None, max_length=512, null=True, upload_to='uploads/hypothesis/%Y/%m/%d/'),
        ),
    ]
