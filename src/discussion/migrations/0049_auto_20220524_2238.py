# Generated by Django 2.2 on 2022-05-24 22:38

from django.db import migrations, models


def add_post_slugs(apps, schema_editor):
    Flag = apps.get_model('discussion', 'flag')

    for flag in Flag.objects.all().iterator():
        if hasattr(flag, 'verdict'):
            veridct = flag.verdict
            flag.verdict_created_date = veridct.created_date
            flag.save()


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0048_auto_20220517_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='verdict_created_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='flag',
            name='reason_choice',
            field=models.CharField(blank=True, choices=[('ABUSIVE_OR_RUDE', 'ABUSIVE_OR_RUDE'), ('COPYRIGHT', 'COPYRIGHT'), ('LOW_QUALITY', 'LOW_QUALITY'), ('NOT_CONSTRUCTIVE', 'NOT_CONSTRUCTIVE'), ('PLAGIARISM', 'PLAGIARISM'), ('SPAM', 'SPAM'), ('NOT_SPECIFIED', 'NOT_SPECIFIED')], max_length=255),
        ),
        migrations.RunPython(add_post_slugs),
    ]
