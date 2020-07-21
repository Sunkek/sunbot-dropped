"""Database models for automatic mgration.

TODO! When Django starts supporting composite primary keys,
rewrite them properly!"""

from django.db import models


class User(models.Model):
    """User model."""
    user_id = models.BigIntegerField(primary_key=True)
    birthday = models.DateField(null=True, blank=True)
    steam = models.URLField(max_length=80, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    ign_ddo = models.CharField(max_length=50, null=True, blank=True)
    ign_warframe_pc = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = "users"


class Guild(models.Model):
    """Settings per guild."""
    guild_id = models.BigIntegerField(primary_key=True)

    birthday_feed_channel_id = models.BigIntegerField(null=True, blank=True)

    track_messages = models.BooleanField(null=True, blank=True, default=False)
    track_reactions = models.BooleanField(null=True, blank=True, default=False)
    track_voice = models.BooleanField(null=True, blank=True, default=False)
    track_games = models.BooleanField(null=True, blank=True, default=False)
    track_emoji = models.BooleanField(null=True, blank=True, default=False)

    mod_junior_role_id = models.BigIntegerField(null=True, blank=True)
    mod_senior_role_id = models.BigIntegerField(null=True, blank=True)
    mod_admin_role_id = models.BigIntegerField(null=True, blank=True)

    mute_role_id = models.BigIntegerField(null=True, blank=True)

    log_general_channel_id = models.BigIntegerField(null=True, blank=True)
    log_mod_channel_id = models.BigIntegerField(null=True, blank=True)
    log_warnings_channel_id = models.BigIntegerField(null=True, blank=True)
    log_karma_channel_id = models.BigIntegerField(null=True, blank=True)

    ad_reminder_channel_id = models.BigIntegerField(null=True, blank=True)
    ad_reminder_ping_role_id = models.BigIntegerField(null=True, blank=True)
    ad_reminder_disboard = models.BooleanField(null=True, blank=True, default=False)
    ad_reminder_disforge = models.BooleanField(null=True, blank=True, default=False)

    karma_positive_emoji = models.CharField(max_length=40, null=True, blank=True)
    karma_negative_emoji = models.CharField(max_length=40, null=True, blank=True)

    warnings_timeout_days = models.PositiveSmallIntegerField(null=True, blank=True)
    warnings_before_mute = models.PositiveSmallIntegerField(null=True, blank=True)
    warnings_before_kick = models.PositiveSmallIntegerField(null=True, blank=True)
    warnings_before_ban = models.PositiveSmallIntegerField(null=True, blank=True)

    welcome_message = models.CharField(max_length=2000, null=True, blank=True)
    welcome_message_embed = models.CharField(max_length=4000, null=True, blank=True)

    verification_message_id = models.BigIntegerField(null=True, blank=True)
    verification_emoji = models.CharField(max_length=40, null=True, blank=True)
    unverified_role_id = models.BigIntegerField(null=True, blank=True)
    verified_role_id = models.BigIntegerField(null=True, blank=True)
    verified_message = models.CharField(max_length=2000, null=True, blank=True)
    verified_message_embed = models.CharField(max_length=4000, null=True, blank=True)

    def __str__(self):
        return str(self.guild_id)

    class Meta:
        db_table = "guilds"


class Messages(models.Model):
    """Info about user's posts - where and how much."""
    guild_id = models.ForeignKey(
        Guild,
        on_delete=models.CASCADE,
        related_name="messages",
        db_column="guild_id",  # Django adds second "_id" otherwise
    )
    channel_id = models.BigIntegerField()
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        db_column="user_id",  # Django adds second "_id" otherwise
    )
    period = models.DateField()
    postcount = models.IntegerField(default=0,)
    attachments = models.IntegerField(default=0,)
    words = models.IntegerField(default=0,)

    def __str__(self):
        return f"{self.guild_id}/{self.channel_id} by {self.user_id} for {self.period}"

    class Meta:
        db_table = "messages"
        # Composite primary key workaround
        unique_together = [["guild_id", "channel_id", "user_id", "period"]]


class Reactions(models.Model):
    """Info about given emoji reactions - who, where and how much."""    
    guild_id = models.ForeignKey(
        Guild,
        on_delete=models.CASCADE,
        related_name="reactions",
        db_column="guild_id",  # Django adds second "_id" otherwise
    )
    giver_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions_given",
        db_column="giver_id",  # Django adds second "_id" otherwise
    )
    receiver_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions_received",
        db_column="receiver_id",  # Django adds second "_id" otherwise
    )
    emoji = models.CharField(max_length=100)
    period = models.DateField()
    count = models.IntegerField(default=0,)

    def __str__(self):
        return f"{self.giver_id} to {self.receiver_id} - {self.emoji} for {self.period}"

    class Meta:
        db_table = "reactions"
        # Composite primary key workaround
        unique_together = [["guild_id", "giver_id", "receiver_id", "emoji", "period"]]


class Games(models.Model):
    """Info about played games - who, when and how much."""
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="games",
        db_column="user_id",  # Django adds second "_id" otherwise
    )
    game = models.CharField(max_length=80, null=True, blank=True)
    period = models.DateField()
    duration = models.IntegerField(default=0,)


    def __str__(self):
        return f"{self.user_id} played {self.game} for {self.duration} at {self.period}"

    class Meta:
        db_table = "games"
        # Composite primary key workaround
        unique_together = [["user_id", "game", "period"]]
