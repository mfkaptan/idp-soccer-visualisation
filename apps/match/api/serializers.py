from rest_framework import serializers

from .. import models


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team


class MatchPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MatchPlayer


class MatchTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    matchplayer_set = MatchPlayerSerializer(many=True)
    class Meta:
        model = models.MatchTeam


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Match
        fields = ['match_id', 'game_title', 'season', 'kickoff_time']


class MatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Match
