# Generated by Django 2.2 on 2022-04-06 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reputation', '0047_auto_20220405_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='token_address',
            field=models.CharField(max_length=255),
        ),
    ]