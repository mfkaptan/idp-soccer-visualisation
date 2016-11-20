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

    half = ["firstHalf", "secondHalf"][int(kwargs["half"])-1]
    minute = kwargs["minute"]
    #lt = kwargs["lte"]
    #gt = kwargs["gt"]

    framesets = FrameSet.objects.all()
    home_framesets = framesets.filter(team=match.home_team, game_section=half)
    away_framesets = framesets.filter(team=match.away_team, game_section=half)
    ball_frameset = framesets.get(match=match, team=None, game_section=half)

    home, away = {}, {}
    for f in home_framesets:
        #home[f.player.shirt_number] = list(f.frame_set.filter(m=54).order_by('n').values('x', 'y', 'n'))
        home[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))
        #home[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))

    for f in away_framesets:
        #away[f.player.shirt_number] = list(f.frame_set.filter(m=54).order_by('n').values('x', 'y', 'n'))
        away[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))
        #away[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))

    #raw_data = serializers.serialize('json', ball_frameset.frame_set.filter(m=54).order_by('n'))
    #raw_data = serializers.serialize('json', ball_frameset.frame_set.filter(m=54).order_by('n'))
    raw_data = serializers.serialize('json', ball_frameset.frame_set.order_by('n'),
                                     fields=('x', 'y', 'z', 'm', 'n', 't'))

    context["ball"] = [d['fields'] for d in json.loads(raw_data)]
    context["home"] = home
    context["away"] = away

    return JsonResponse(context)
