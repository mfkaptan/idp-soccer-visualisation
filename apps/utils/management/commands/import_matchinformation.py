from lxml import etree

from django.core.management.base import BaseCommand, CommandError
from django.db import models

from apps.match.models import *


class Command(BaseCommand):
    help = 'Imports given match information xml to database'
    MATCH_ID = None

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def create_match(self):
        match, created = Match.objects.get_or_create(match_id=self.MATCH_ID)
        if created:
            match.save()

        return match

    def create_match_team(self, team_id):
        match = self.create_match()
        team, created = Team.objects.get_or_create(team_id=team_id)
        if created:
            team.save()

        match_team, created = MatchTeam.objects.get_or_create(team_id=team_id, match_id=self.MATCH_ID)
        if created:
            match_team.save()

        return match_team

    # Match xml attributes with object attributes from verbose names
    def object_from_elem(self, obj, e):
        d = {}
        # Get {f.verbose_name: f.name}
        for f in obj._meta.get_fields():
            if not f.many_to_one and f.related_model is None:
                d[f.verbose_name] = f.name

        for tag in e.keys():
            if tag in d and hasattr(obj, d[tag]):
                field = obj._meta.get_field(d[tag])
                if isinstance(field, models.IntegerField):
                    setattr(obj, d[tag], int(e.get(tag)))
                elif isinstance(field, models.FloatField):
                    setattr(obj, d[tag], float(e.get(tag)))
                elif isinstance(field ,models.NullBooleanField):
                    setattr(obj, d[tag], e.get(tag).lower() == "true")
                else:
                    setattr(obj, d[tag], e.get(tag))

    def process(self, e):
        if e.tag == "General":
            self.MATCH_ID = e.get("MatchId")

            m = Match.objects.get_or_create(match_id=self.MATCH_ID)[0]
            self.object_from_elem(m, e)
            m.save()

        elif e.tag == "Environment":
            stadium = Stadium.objects.get_or_create(stadium_id=e.get("StadiumId"))[0]
            self.object_from_elem(stadium, e)
            stadium.save()

            ms = MatchStadium.objects.get_or_create(stadium_id=stadium.stadium_id)[0]
            ms.stadium = stadium

            ms.match = self.create_match()
            self.object_from_elem(ms, e)
            ms.save()

        elif e.tag == "Team":
            team_id = e.get("TeamId")

            team = Team.objects.get_or_create(team_id=team_id)[0]
            team.name=e.get("TeamName")
            team.save()

            mt = self.create_match_team(team_id)
            mt.team = team
            self.object_from_elem(mt, e)
            mt.save()

        elif e.tag == "Player":
            team_id = e.getparent().getparent().get("TeamId")

            player = Player.objects.get_or_create(player_id=e.get("PersonId"))[0]
            self.object_from_elem(player, e)
            player.save()

            # First, get or create
            match_team = self.create_match_team(team_id)

            mp = MatchPlayer.objects.get_or_create(player_id=player.player_id, match_team__team_id=team_id)[0]
            mp.player = player
            mp.match_team = match_team
            self.object_from_elem(mp, e)
            mp.save()

        elif e.tag == "Trainer" or e.tag == "Official":
            team_id = e.getparent().getparent().get("TeamId")

            p = Person.objects.get_or_create(person_id=e.get("PersonId"))[0]

            p.match_team = self.create_match_team(team_id)
            self.object_from_elem(p, e)
            p.job = e.tag.lower()
            p.save()

        elif e.tag == "Referee":
            r = Referee.objects.get_or_create(person_id=e.get("PersonId"))[0]

            r.match = self.create_match()
            self.object_from_elem(r, e)
            r.save()

        elif e.tag == "OtherGameInformation":
            m = Match.objects.get_or_create(match_id=self.MATCH_ID)[0]
            self.object_from_elem(m, e)
            m.save()

    def fast_iter(self, context):
        for event, elem in context:
            self.process(elem)
            elem.clear()

            for ancestor in elem.xpath('ancestor-or-self::*'):
                #print('Checking ancestor: {a}'.format(a=ancestor.tag))
                while ancestor.getprevious() is not None:
                    #print('Deleting {p}'.format(p=(ancestor.getparent()[0]).tag))
                    del ancestor.getparent()[0]
        del context

    def handle(self, *args, **options):
        context = etree.iterparse(options['file'])
        self.fast_iter(context)

