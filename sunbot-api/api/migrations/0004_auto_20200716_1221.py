# Generated by Django 3.0.8 on 2020-07-16 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200714_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('guild_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('birthday_feed_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('track_messages', models.BooleanField(blank=True, default=False, null=True)),
                ('track_reactions', models.BooleanField(blank=True, default=False, null=True)),
                ('track_voice', models.BooleanField(blank=True, default=False, null=True)),
                ('track_games', models.BooleanField(blank=True, default=False, null=True)),
                ('mod_junior_role_id', models.BigIntegerField(blank=True, null=True)),
                ('mod_senior_role_id', models.BigIntegerField(blank=True, null=True)),
                ('mod_admin_role_id', models.BigIntegerField(blank=True, null=True)),
                ('mute_role_id', models.BigIntegerField(blank=True, null=True)),
                ('log_general_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('log_mod_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('log_warnings_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('log_karma_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('ad_reminder_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('ad_reminder_ping_role_id', models.BigIntegerField(blank=True, null=True)),
                ('ad_reminder_disboard', models.BooleanField(blank=True, default=False, null=True)),
                ('ad_reminder_disforge', models.BooleanField(blank=True, default=False, null=True)),
                ('karma_positive_emoji', models.CharField(blank=True, max_length=40, null=True)),
                ('karma_negative_emoji', models.CharField(blank=True, max_length=40, null=True)),
                ('warnings_timeout_days', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('warnings_before_mute', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('warnings_before_kick', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('warnings_before_ban', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('welcome_message', models.CharField(blank=True, max_length=2000, null=True)),
                ('welcome_message_embed', models.CharField(blank=True, max_length=4000, null=True)),
                ('verification_message_id', models.BigIntegerField(blank=True, null=True)),
                ('verification_emoji', models.CharField(blank=True, max_length=40, null=True)),
                ('unverified_role_id', models.BigIntegerField(blank=True, null=True)),
                ('verified_role_id', models.BigIntegerField(blank=True, null=True)),
                ('verified_message', models.CharField(blank=True, max_length=2000, null=True)),
                ('verified_message_embed', models.CharField(blank=True, max_length=4000, null=True)),
            ],
            options={
                'db_table': 'guilds',
            },
        ),
        migrations.AlterField(
            model_name='messages',
            name='guild_id',
            field=models.ForeignKey(db_column='guild_id', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.Guild'),
        ),
    ]
