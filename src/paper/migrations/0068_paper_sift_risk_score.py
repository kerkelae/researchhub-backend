# Generated by Django 2.2 on 2020-11-06 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0067_auto_20201104_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='sift_risk_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]