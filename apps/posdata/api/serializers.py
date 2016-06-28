from rest_framework import serializers

from .. import models


class FrameSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrameSet


class FrameSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    def get_player(self, obj):
        try:
            return obj.set.player.shirt_number
        except:
            return 0

    def get_team(self, obj):
        try:
            return obj.set.team.role
        except:
            return "ball"

    class Meta:
        model = models.Frame
