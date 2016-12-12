from django.db import models
from django.utils.functional import cached_property
from django.contrib.contenttypes.models import ContentType


class Match(models.Model):
    match_id = models.CharField("MatchId", max_length=50, primary_key=True)
    competition = models.CharField("Competition", null=True, max_length=50)
    competition_id = models.CharField("CompetitionId", null=True, max_length=50)
    dl_provider_id = models.CharField("DL-PROVIDER-ID",null=True, max_length=50)
    game_title = models.CharField("GameTitle", null=True, max_length=200)
    host = models.CharField("Host", null=True, max_length=200)
    kickoff_time = models.DateTimeField("KickoffTime", null=True, )
    planned_kickoff_time = models.DateTimeField("PlannedKickoffTime", null=True, )
    match_day = models.IntegerField("MatchDay", null=True, )
    season = models.CharField("Season", null=True, max_length=50)
    match_type = models.CharField("Type", null=True, max_length=50)
    sport_type = models.CharField("TypeOfSport", null=True, max_length=50)
    playing_time_first_half = models.IntegerField("PlayingTimeFirstHalf", null=True, blank=True)
    playing_time_second_half = models.IntegerField("PlayingTimeSecondHalf", null=True, blank=True)
    total_time_first_half = models.IntegerField("TotalTimeFirstHalf", null=True, blank=True)
    total_time_second_half = models.IntegerField("TotalTimeSecondHalf", null=True, blank=True)

    @cached_property
    def home_team(self):
        return self.matchteam_set.get(role="home")

    @cached_property
    def away_team(self):
        return self.matchteam_set.get(role="guest")

    @cached_property
    def get_score(self):
        return self.get_goals[-1].content_object.content_object.current_result
        
    @cached_property
    def get_goals(self):
        shots = self.get_shots
        return [g for g in shots if g.content_object.content_type.model == "successfulshot"]

    @cached_property
    def get_shots(self):
        return self.event_set.filter(content_type__model="shotatgoal").order_by("time")

    def __str__(self):
        return self.game_title


class Stadium(models.Model):
    stadium_id = models.CharField("StadiumId", max_length=50, primary_key=True)
    name = models.CharField("StadiumName", null=True, max_length=100)
    capacity = models.IntegerField("StadiumCapacity", null=True, )
    pitch_x = models.FloatField("PitchX", null=True, )
    pitch_y = models.FloatField("PitchY", null=True, )
    adress = models.CharField("Address", null=True, max_length=200)
    country = models.CharField("Country", null=True, max_length=50)

    def get_matches(self):
        matches = []
        played = self.matchstadium_set.all()
        for p in played:
            matches.append(p.match)

        return matches

    def __str__(self):
        return self.name


class MatchStadium(models.Model):
    floodlight = models.CharField("Floodlight", null=True, max_length=20)
    pitch_erosion = models.CharField("PitchErosion", null=True, max_length=50)
    precipitation = models.CharField("Precipitation", null=True, max_length=50)
    roof = models.CharField("Roof", null=True, max_length=20)
    soldout = models.NullBooleanField("SoldOut", null=True, )
    temperature = models.IntegerField("Temperature", null=True, )
    number_of_spectators = models.IntegerField("NumberOfSpectators", null=True, )
    air_humidity = models.IntegerField("AirHumidity", null=True, )
    air_pressure = models.IntegerField("AirPressure", null=True, )

    stadium = models.ForeignKey(Stadium, null=True)
    match = models.OneToOneField(Match, null=True)

    def __str__(self):
        try:
            return self.stadium.name
        except:
            return "MatchStadium"

    class Meta:
        unique_together = ('stadium', 'match')


class Team(models.Model):
    team_id = models.CharField("TeamId", max_length=50, primary_key=True)
    name = models.CharField("TeamName", null=True, max_length=50)

    def get_matches(self):
        matches = []
        played = self.matchteam_set.all()
        for p in played:
            matches.append(p.match)

        return matches

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return "Team"


class MatchTeam(models.Model):
    main_color = models.CharField("PlayerMainColorOfShirt", null=True, max_length=7)
    other_color = models.CharField("PlayerOtherColorOfShirt", null=True, max_length=7)
    role = models.CharField("Role", null=True, max_length=6)

    team = models.ForeignKey(Team, null=True)
    match = models.ForeignKey(Match, null=True)

    @cached_property
    def name(self):
        return self.team.name

    def get_players(self):
        return self.matchplayer_set.all()

    def get_trainer_staff(self):
        return self.person_set.filter(job="trainer")

    def get_official_staff(self):
        return self.person_set.filter(job="official")

    def __str__(self):
        try:
            return self.team.name
        except:
            return "MatchTeam"

    class Meta:
        unique_together = ('team', 'match')


class Person(models.Model):
    person_id = models.CharField("PersonId", max_length=50, primary_key=True)
    first_name = models.CharField("FirstName", null=True, max_length=50)
    last_name = models.CharField("LastName", null=True, max_length=50)
    short_name = models.CharField("Shortname", null=True, max_length=50)
    role = models.CharField("Role", null=True, max_length=50)

    job = models.CharField(null=True, max_length=50)

    match_team = models.ForeignKey(MatchTeam, null=True)

    def __str__(self):
        return self.job + " " + self.short_name


class Referee(models.Model):
    person_id = models.CharField("PersonId", max_length=50, primary_key=True)
    first_name = models.CharField("FirstName", null=True, max_length=50)
    last_name = models.CharField("LastName", null=True, max_length=50)
    short_name = models.CharField("Shortname", null=True, max_length=50)
    role = models.CharField("Role", null=True, max_length=50)

    match = models.ForeignKey(Match, null=True)

    def __str__(self):
        return self.role + " " + self.short_name


class Player(models.Model):
    player_id = models.CharField("PersonId", max_length=50, primary_key=True)
    first_name = models.CharField("FirstName", null=True, max_length=50)
    last_name = models.CharField("LastName", null=True, max_length=50)
    short_name = models.CharField("Shortname", null=True, max_length=50)

    def get_matches(self):
        matches = []
        played = self.matchplayer_set.all()
        for p in played:
            matches.append(p.team.match)

        return matches

    def __str__(self):
        return self.short_name


class MatchPlayer(models.Model):
    playing_position = models.CharField("PlayingPosition", null=True, max_length=5)
    team_leader = models.NullBooleanField("TeamLeader", null=True, )
    shirt_number = models.IntegerField("ShirtNumber", null=True, )
    starting = models.NullBooleanField("Starting", null=True, )

    player = models.ForeignKey(Player, null=True)
    match_team = models.ForeignKey(MatchTeam, null=True)

    @cached_property
    def name(self):
        return self.player.short_name

    def __str__(self):
        try:
            return self.player.short_name
        except:
            return "MatchPlayer"

    class Meta:
        unique_together = ('player', 'match_team')
