import json

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.template import Context
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from .models import Match
from apps.posdata.models import FrameSet


class MatchList(ListView):
    model = Match


class MatchDetail(TemplateView):
    template_name = "match/match_detail.html"


    def filter_and_serialize(self, frame_set, min, ball=False):
        fields = ['t', 'x', 'y', 's', 'm']
        if ball:
            fields.append('z')

        temp_output = serializers.serialize('python', frame_set.filter(m=min).order_by('n')[::25], fields=fields)

        return json.dumps(temp_output, cls=DjangoJSONEncoder)

    def get_context_data(self, **kwargs):
        context = super(MatchDetail, self).get_context_data(**kwargs)

        match = Match.objects.get(pk=kwargs["pk"])
        framesets = FrameSet.objects.all()
        home_first_half = framesets.filter(team=match.home_team, game_section="firstHalf")
        home_second_half = framesets.filter(team=match.home_team, game_section="secondHalf")
        away_first_half = framesets.filter(team=match.away_team, game_section="firstHalf")
        away_second_half = framesets.filter(team=match.away_team, game_section="secondHalf")

        ball_first_half = framesets.get(match=match, team=None, game_section="firstHalf")
        ball_second_half = framesets.get(match=match, team=None, game_section="secondHalf")

        h1, a1, h2, a2, data = {}, {}, {}, {}, {}
        for f in home_first_half:
            h1[f.player.shirt_number] = self.filter_and_serialize(f.frame_set, 1)

        for f in home_second_half:
            h2[f.player.shirt_number] = self.filter_and_serialize(f.frame_set, 1)

        for f in away_first_half:
            a1[f.player.shirt_number] = self.filter_and_serialize(f.frame_set, 1)

        for f in away_second_half:
            a2[f.player.shirt_number] = self.filter_and_serialize(f.frame_set, 1)

        data["ball_first_half"] = {}
        data["ball_second_half"] = {}

        data["ball_first_half"][0] = self.filter_and_serialize(ball_first_half.frame_set , 1, True)
        data["ball_second_half"][0] = self.filter_and_serialize(ball_second_half.frame_set , 1, True)

        data["home_first_half"] = h1
        data["away_first_half"] = a1
        data["home_second_half"] = h2
        data["away_second_half"] = a2
        context["match"] = match
        context["data"] = data

        print("Data is ready")
        return context
