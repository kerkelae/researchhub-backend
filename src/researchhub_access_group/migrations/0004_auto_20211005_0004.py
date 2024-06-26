# Generated by Django 2.2 on 2021-10-05 00:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('researchhub_access_group', '0003_auto_20210603_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researchhubaccessgroup',
            name='admins',
        ),
        migrations.RemoveField(
            model_name='researchhubaccessgroup',
            name='editors',
        ),
        migrations.RemoveField(
            model_name='researchhubaccessgroup',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='researchhubaccessgroup',
            name='viewers',
        ),
        migrations.AddField(
            model_name='researchhubaccessgroup',
            name='key',
            field=models.CharField(default='key', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='researchhubaccessgroup',
            name='name',
            field=models.CharField(default='VIEWER', max_length=32),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('access_type', models.CharField(choices=[('ADMIN', 'ADMIN'), ('EDITOR', 'EDITOR'), ('VIEWER', 'VIEWER')], default='VIEWER', max_length=8)),
                ('access_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='researchhub_access_group.ResearchhubAccessGroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
