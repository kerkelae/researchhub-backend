# Generated by Django 2.2 on 2020-11-19 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0069_remove_paper_sift_risk_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='is_removed_by_user',
            field=models.BooleanField(default=False, help_text='Hides the paper because it is not allowed.'),
        ),
    ]