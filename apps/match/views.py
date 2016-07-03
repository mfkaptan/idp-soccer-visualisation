import json
# from timeit import default_timer as timer

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.template import Context
from django.core import serializers

from .models import Match
from apps.posdata.models import FrameSet


class MatchList(ListView):
    model = Match


class MatchDetail(TemplateView):
    template_name = "match/match_detail.html"

    def get_context_data(self, **kwargs):
        context = {}

        match = Match.objects.get(pk=kwargs["pk"])
        framesets = FrameSet.objects.all()

        home_framesets = framesets.filter(team=match.home_team, game_section="firstHalf")
        away_framesets = framesets.filter(team=match.away_team, game_section="firstHalf")
        ball_frameset = framesets.get(match=match, team=None, game_section="firstHalf")

        home, away, data = {}, {}, {}
        for f in home_framesets:
            #home[f.player.shirt_number] = list(f.frame_set.filter(m=54).order_by('n').values('x', 'y', 'n'))
            home[f.player.shirt_number] = list(f.frame_set.filter(m__lt=15).order_by('n').values('x', 'y', 'n'))
            #home[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))

        for f in away_framesets:
            #away[f.player.shirt_number] = list(f.frame_set.filter(m=54).order_by('n').values('x', 'y', 'n'))
            away[f.player.shirt_number] = list(f.frame_set.filter(m__lt=15).order_by('n').values('x', 'y', 'n'))
            #away[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))

        #raw_data = serializers.serialize('json', ball_frameset.frame_set.filter(m=54).order_by('n'))
        raw_data = serializers.serialize('json', ball_frameset.frame_set.filter(m__lt=15).order_by('n'),
                                         fields=('x', 'y', 'z', 'm', 'n', 't'))
        #raw_data = serializers.serialize('json', ball_frameset.frame_set.order_by('n'))

        data["ball"] = [d['fields'] for d in json.loads(raw_data)]
        data["home"] = home
        data["away"] = away
        context["match"] = match
        context["data"] = data

        # start = timer()
        # end = timer()
        # print(end-start)

        print("Data is ready")
        return context
