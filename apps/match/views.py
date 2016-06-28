import json

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.template import Context
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from .models import Match
from apps.posdata.models import FrameSet


class MatchList(ListView):
    model = Match


class MatchDetail(TemplateView):
    template_name = "match/match_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MatchDetail, self).get_context_data(**kwargs)

        match = Match.objects.get(pk=kwargs["pk"])
        framesets = FrameSet.objects.all()

        home_framesets = framesets.filter(team=match.home_team, game_section="secondHalf")
        away_framesets = framesets.filter(team=match.away_team, game_section="secondHalf")
        ball_frameset = framesets.get(match=match, team=None, game_section="secondHalf")

        home, away, data = {}, {}, {}
        for f in home_framesets:
            home[f.player.shirt_number] = list(f.frame_set.filter(m=54).order_by('n').values('x', 'y'))
            #home[f.player.shirt_number] = list(f.frame_set.filter(m__lt=60).order_by('n').values('x', 'y'))

        for f in away_framesets:
            away[f.player.shirt_number] = list(f.frame_set.filter(m=54).order_by('n').values('x', 'y'))
            #away[f.player.shirt_number] = list(f.frame_set.filter(m__lt=60).order_by('n').values('x', 'y'))

        data["ball"] = list(ball_frameset.frame_set.filter(m=54).order_by('n').values('x', 'y', 'z'))
        #data["ball"] = list(ball_frameset.frame_set.filter(m__lt=60).order_by('n').values('x', 'y', 'z'))

        data["home"] = home
        data["away"] = away
        context["match"] = match
        context["data"] = data

        print("Data is ready")
        return context



