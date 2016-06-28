import json

from django.shortcuts import render
from django.template import Context
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from apps.posdata.models import Match
from .models import FrameSet


def get_data(request, **kwargs):
    context = {}

    match = Match.objects.get(pk=kwargs["pk"])
    half = kwargs["half"]
    minute = kwargs["minute"]

    framesets = FrameSet.objects.all()
    home_framesets = framesets.filter(team=match.home_team, game_section=half)
    away_framesets = framesets.filter(team=match.away_team, game_section=half)
    ball_frameset = framesets.get(match=match, team=None, game_section=half)

    home, away, data = {}, {}, {}

    for f in home_framesets:
        home[f.player.shirt_number] = list(f.frame_set.filter(m=minute).order_by('n').values('x', 'y'))

    for f in away_framesets:
        away[f.player.shirt_number] = list(f.frame_set.filter(m=minute).order_by('n').values('x', 'y'))

    data["ball"] = list(ball_frameset.frame_set.filter(m=minute).order_by('n').values('x', 'y'))
    data["home"] = home
    data["away"] = away
    context["data"] = data

    return JsonResponse(context)
