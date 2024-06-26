# Generated by Django 2.2 on 2022-09-22 18:15

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
from django.contrib.postgres.operations import HStoreExtension


def migrate_notifications(apps, schema_editor):
    Notification = apps.get_model('notification', 'notification')

    for notification in Notification.objects.all().iterator():
        action = notification.action
        action_model = action.content_type.model

        notification.object_id = action.object_id
        notification.content_type = action.content_type
        if action_model == 'thread':
            notification.notification_type = 'THREAD_ON_DOC'
        elif action_model == 'comment':
            notification.notification_type = 'COMMENT_ON_THREAD'
        elif action_model == 'reply':
            notification.notification_type = 'REPLY_ON_THREAD'
        elif action_model == 'bounty':
            notification.notification_type = 'BOUNTY_EXPIRING_SOON'
        elif action_model == 'purchase':
            notification.notification_type = 'RSC_SUPPORT_ON_DOC'
        elif action_model == 'verdict':
            notification.notification_type = 'FLAGGED_CONTENT_VERDICT'
        elif action_model == 'withdrawal':
            notification.notification_type = 'RSC_WITHDRAWAL_COMPLETE'
        elif action_model == 'verdict':
            notification.notification_type = 'FLAGGED_CONTENT_VERDICT'
        else:
            notification.notification_type = 'DEPRECATED'
            notification.object_id = 1
            notification.content_type_id = 6
        notification.save()


def format_notifications(apps, schema_editor):
    Notification = apps.get_model('notification', 'notification')

    for notification in Notification.objects.all().iterator():
        try:
            notification.save()
        except Exception as e:
            print(e)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notification', '0009_remove_notification_extra'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='notification',
            name='body',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.hstore.HStoreField(), default=list, size=None),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('DEPRECATED', 'DEPRECATED'), ('THREAD_ON_DOC', 'THREAD_ON_DOC'), ('COMMENT_ON_THREAD', 'COMMENT_ON_THREAD'), ('REPLY_ON_THREAD', 'REPLY_ON_THREAD'), ('RSC_WITHDRAWAL_COMPLETE', 'RSC_WITHDRAWAL_COMPLETE'), ('RSC_SUPPORT_ON_DOC', 'RSC_SUPPORT_ON_DOC'), ('RSC_SUPPORT_ON_DIS', 'RSC_SUPPORT_ON_DIS'), ('FLAGGED_CONTENT_VERDICT', 'FLAGGED_CONTENT_VERDICT'), ('BOUNTY_EXPIRING_SOON', 'BOUNTY_EXPIRING_SOON'), ('DIS_ON_BOUNTY', 'DIS_ON_BOUNTY')], max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='notification',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='navigation_url',
            field=models.URLField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='extra',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict),
        ),
        migrations.RunPython(migrate_notifications),
        migrations.AlterField(
            model_name='notification',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.RemoveField(
            model_name='notification',
            name='action',
        ),
        migrations.RunPython(format_notifications),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['content_type', 'object_id'], name='notificatio_content_743343_idx'),
        ),
    ]
