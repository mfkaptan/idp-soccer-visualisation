from lxml import etree

from django.core.management.base import BaseCommand, CommandError

from posdata.models import *


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
            print(team)

        match_team, created = MatchTeam.objects.get_or_create(team_id=team_id, match_id=self.MATCH_ID)
        if created:
            match_team.save()

        return match_team

    def process(self, e):
        if e.tag == "General":
            self.MATCH_ID = e.get("MatchId")

            m = Match.objects.get_or_create(match_id=self.MATCH_ID)[0]
            m.competition = e.get("Competition")
            m.competition_id = e.get("CompetitionId")
            m.dl_provider_id = e.get("DL-PROVIDER-ID")
            m.game_title = e.get("GameTitle")
            m.host = e.get("Host")
            m.kickoff_time = e.get("KickoffTime")
            m.planned_kickoff_time = e.get("PlannedKickoffTime")
            m.match_day = e.get("MatchDay")
            m.season = e.get("Season")
            m.match_type = e.get("Type")
            m.sport_type = e.get("TypeOfSport")
            m.save()

        elif e.tag == "Environment":
            stadium = Stadium.objects.get_or_create(stadium_id=e.get("StadiumId"))[0]
            stadium.name = e.get("StadiumName")
            stadium.country = e.get("Country")
            stadium.adress = e.get("Address")
            stadium.pitch_x = float(e.get("PitchX"))
            stadium.pitch_y = float(e.get("PitchY"))
            stadium.capacity = e.get("StadiumCapacity")
            stadium.save()

            ms = MatchStadium.objects.get_or_create(stadium_id=stadium.stadium_id)[0]
            ms.stadium = stadium

            ms.match = self.create_match()
            ms.floodlight = e.get("Floodlight")
            ms.pitch_erosion = e.get("PitchErosion")
            ms.precipitation = e.get("Precipitation")
            ms.roof = e.get("Roof")
            ms.soldout = (e.get("SoldOut").lower() == "true")
            ms.temperature = int(e.get("Temperature"))
            ms.number_of_spectators = int(e.get("NumberOfSpectators"))
            ms.air_humidity = int(e.get("AirHumidity"))
            ms.air_pressure = int(e.get("AirPressure"))
            ms.save()

        elif e.tag == "Team":
            team_id = e.get("TeamId")

            team = Team.objects.get_or_create(team_id=team_id)[0]
            team.name=e.get("TeamName")
            team.save()

            mt = self.create_match_team(team_id)
            mt.team = team
            mt.main_color = e.get("PlayerMainColorOfShirt")
            mt.other_color = e.get("PlayerOtherColorOfShirt")
            mt.role = e.get("Role")
            mt.save()

        elif e.tag == "Player":
            team_id = e.getparent().getparent().get("TeamId")

            player = Player.objects.get_or_create(player_id=e.get("PersonId"))[0]
            player.first_name = e.get("FirstName")
            player.last_name = e.get("LastName")
            player.short_name = e.get("Shortname")
            player.save()

            # First, get or create
            match_team = self.create_match_team(team_id)

            mp = MatchPlayer.objects.get_or_create(player_id=player.player_id, match_team__team_id=team_id)[0]
            mp.player = player
            mp.match_team = match_team
            mp.playing_position = e.get("PlayingPosition")
            mp.team_leader = (e.get("TeamLeader").lower() == "true")
            mp.starting = (e.get("Starting").lower() == "true")
            mp.shirt_number = int(e.get("ShirtNumber"))
            mp.save()

        elif e.tag == "Trainer" or e.tag == "Official":
            team_id = e.getparent().getparent().get("TeamId")

            p = Person.objects.get_or_create(person_id=e.get("PersonId"))[0]

            p.match_team = self.create_match_team(team_id)
            p.first_name = e.get("FirstName")
            p.last_name = e.get("LastName")
            p.short_name = e.get("Shortname")
            p.job = e.tag.lower()
            p.role = e.get("Role")
            p.save()

        elif e.tag == "Referee":
            r = Referee.objects.get_or_create(person_id=e.get("PersonId"))[0]

            r.match = self.create_match()
            r.first_name = e.get("FirstName")
            r.last_name = e.get("LastName")
            r.short_name = e.get("Shortname")
            r.role = e.get("Role")
            r.save()

        elif e.tag == "OtherGameInformation":
            m = Match.objects.get_or_create(match_id=self.MATCH_ID)[0]
            m.playing_time_first_half = int(e.get("PlayingTimeFirstHalf"))
            m.playing_time_second_half = int(e.get("PlayingTimeSecondHalf"))
            m.total_time_first_half = int(e.get("TotalTimeFirstHalf"))
            m.total_time_second_half = int(e.get("TotalTimeSecondHalf"))
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

