import json

from django.core.management.base import BaseCommand
from django.core import serializers

from apps.match.models import Match
from apps.posdata.models import FrameSet


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = {}

        match = Match.objects.first()

        framesets = FrameSet.objects.all()
        home_framesets = framesets.filter(team=match.home_team, game_section="firstHalf")
        away_framesets = framesets.filter(team=match.away_team, game_section="firstHalf")
        ball_frameset = framesets.get(match=match, team=None, game_section="firstHalf")

        home, away = {}, {}
        for f in home_framesets:
            home[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))

        for f in away_framesets:
            away[f.player.shirt_number] = list(f.frame_set.order_by('n').values('x', 'y', 'n'))

        raw_data = serializers.serialize('json', ball_frameset.frame_set.order_by('n'),
                                         fields=('x', 'y', 'z', 'm', 'n', 't'))

        data["ball"] = [d['fields'] for d in json.loads(raw_data)]
        data["home"] = home
        data["away"] = away

        with open(str(match.pk)+".json", "w") as outfile:
            json.dump(data, outfile, separators=(',', ':'))
