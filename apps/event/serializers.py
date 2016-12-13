from django.db import models

from rest_framework import serializers as rest_serializers

from .models import *


class ShotEventSerializer(rest_serializers.ModelSerializer):
    shot = rest_serializers.SerializerMethodField()

    def get_shot(self, obj):
        return ShotAtGoalSerializer(obj.content_object).data

    class Meta:
        model = Event
        exclude = ["content_type"]


class ShotAtGoalSerializer(rest_serializers.ModelSerializer):
    team = rest_serializers.SerializerMethodField()
    player = rest_serializers.SerializerMethodField()
    type = rest_serializers.SerializerMethodField()
    attrs = rest_serializers.SerializerMethodField()

    def get_team(self, obj):
        return "home" if obj.team.role == "home" else "away"

    def get_player(self, obj):
        return obj.player.shirt_number

    def get_type(self, obj):
        return obj.content_type.model

    def get_attrs(self, obj):
        mdl = obj.content_type.model
        if mdl == "savedshot":
            return SavedShotSerializer(obj.content_object).data
        elif mdl == "successfulshot":
            return SuccessfulShotSerializer(obj.content_object).data
        elif mdl == "blockedshot":
            return BlockedShotSerializer(obj.content_object).data
        elif mdl == "shotwide":
            return ShotWideSerializer(obj.content_object).data

    class Meta:
        model = ShotAtGoal
        exclude = ["content_type", "ball_possession_phase", "after_free_kick"]


class SavedShotSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = SavedShot


class SuccessfulShotSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = SuccessfulShot


class BlockedShotSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = BlockedShot


class ShotWideSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = ShotWide


class ShotWoodWorkSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = ShotWoodWork
