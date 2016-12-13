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


class PlayEventSerializer(rest_serializers.ModelSerializer):
    play = rest_serializers.SerializerMethodField()

    def get_play(self, obj):
        return PlaySerializer(obj.content_object).data

    class Meta:
        model = Event
        exclude = ["content_type"]


class PlaySerializer(rest_serializers.ModelSerializer):
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
        if mdl == "pass":
            return PassSerializer(obj.content_object).data
        elif mdl == "cross":
            return CrossSerializer(obj.content_object).data

    class Meta:
        model = Play
        exclude = ["content_type", "ball_possession_phase"]


class PassSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = Pass


class CrossSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = Cross


class SubstitutionEventSerializer(rest_serializers.ModelSerializer):
    substitution = rest_serializers.SerializerMethodField()

    def get_substitution(self, obj):
        return SubstitutionSerializer(obj.content_object).data

    class Meta:
        model = Event
        exclude = ["content_type"]


class SubstitutionSerializer(rest_serializers.ModelSerializer):
    player_in = rest_serializers.SerializerMethodField()
    player_out = rest_serializers.SerializerMethodField()
    team = rest_serializers.SerializerMethodField()

    def get_player_in(self, obj):
        return obj.player_in.shirt_number

    def get_player_out(self, obj):
        return obj.player_out.shirt_number

    def get_team(self, obj):
        return "home" if obj.team.role == "home" else "away"

    class Meta:
        model = Substitution


class CautionEventSerializer(rest_serializers.ModelSerializer):
    caution = rest_serializers.SerializerMethodField()

    def get_caution(self, obj):
        return CautionSerializer(obj.content_object).data

    class Meta:
        model = Event
        exclude = ["content_type"]


class CautionSerializer(rest_serializers.ModelSerializer):
    team = rest_serializers.SerializerMethodField()
    player = rest_serializers.SerializerMethodField()

    def get_player(self, obj):
        return obj.player.shirt_number

    def get_team(self, obj):
        return "home" if obj.team.role == "home" else "away"

    class Meta:
        model = Caution


class FoulEventSerializer(rest_serializers.ModelSerializer):
    foul = rest_serializers.SerializerMethodField()

    def get_foul(self, obj):
        return FoulSerializer(obj.content_object).data

    class Meta:
        model = Event
        exclude = ["content_type"]


class FoulSerializer(rest_serializers.ModelSerializer):
    team_fouler = rest_serializers.SerializerMethodField()
    team_fouled = rest_serializers.SerializerMethodField()
    fouler = rest_serializers.SerializerMethodField()
    fouled = rest_serializers.SerializerMethodField()

    def get_fouler(self, obj):
        return obj.fouler.shirt_number

    def get_fouled(self, obj):
        return obj.fouled.shirt_number

    def get_team_fouler(self, obj):
        return "home" if obj.team_fouler.role == "home" else "away"

    def get_team_fouled(self, obj):
        return "home" if obj.team_fouled.role == "home" else "away"

    class Meta:
        model = Foul