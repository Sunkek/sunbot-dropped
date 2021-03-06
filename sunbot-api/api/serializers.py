from rest_framework import serializers, pagination

from .models import User, Guild, Messages, Reactions, Games, Voice, Emotes, \
    Activity, Nwords


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        exclude = ["id"]  # Useless primary key field
        

class MessagesTopSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    class Meta:
        model = Messages
        fields = ["user_id", "count"]


class ReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        exclude = ["id"]  # Useless primary key field


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        exclude = ["id"]  # Useless primary key field


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        exclude = ["id"]  # Useless primary key field


class EmotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotes
        exclude = ["id"]  # Useless primary key field


class EmotesTopSerializer(serializers.ModelSerializer):
    emote = serializers.CharField()
    message_count = serializers.IntegerField()
    reaction_count = serializers.IntegerField()
    total_count = serializers.IntegerField()
    
    class Meta:
        model = Messages
        fields = ["emote", "message_count", "reaction_count", "total_count"]

                
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ["id"]  # Useless primary key field


class ActivityTopSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    class Meta:
        model = Activity
        fields = ["user_id", "count"]

        
class NwordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nwords
        exclude = ["id"]  # Useless primary key field
        

class NwordsTopSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    nigger_count = serializers.IntegerField()
    nigga_count = serializers.IntegerField()
    total_count = serializers.IntegerField()
    
    class Meta:
        model = Nwords
        fields = ["user_id", "nigger_count", "nigga_count", "total_count"]