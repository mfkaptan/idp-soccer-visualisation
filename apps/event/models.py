from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.match.models import Match, MatchTeam, MatchPlayer


class EventElement(models.Model):
    def __str__(self):
        return self.__class__.__name__

    class Meta:
        abstract = True


class Event(models.Model):
    event_id = models.CharField("EventId", max_length=50, primary_key=True)
    time = models.DateTimeField("EventTime", null=True)
    match = models.ForeignKey(Match)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        try:
            return str(self.content_type)
        except:
            return "Event"


class Substitution(EventElement):
    player_out = models.ForeignKey(MatchPlayer, null=True, verbose_name='PlayerOut', related_name='player_out+')
    player_in = models.ForeignKey(MatchPlayer, null=True, verbose_name='PlayerIn', related_name='player_in+')
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    playing_position = models.CharField(max_length=50, null=True, verbose_name='PlayingPosition')

    def __str__(self):
        try:
            s = str.format("Substitution For: {team}, Out: {p_out} | In: {p_in}",
                           team.name, player_out, player_in)
        except:
            return "Substitution"


class RefereeSubstitution(EventElement):
    referee_in = models.CharField(max_length=50, null=True, verbose_name='RefereeIn')
    referee_out = models.CharField(max_length=50, null=True, verbose_name='RefereeOut')


class RefereeBall(EventElement):
    pass


class OtherRefereeAction(EventElement):
    reason = models.CharField(max_length=50, null=True, verbose_name='Reason')
    start_time = models.DateTimeField(null=True, verbose_name='StartTime')
    end_time = models.DateTimeField(null=True, verbose_name='EndTime')


class Caution(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    card_color = models.CharField(max_length=50, null=True, verbose_name='CardColor')


class SendingOff(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')


class KickoffWhistle(EventElement):
    game_section = models.CharField(max_length=50, null=True, verbose_name='GameSection')


class FinalWhistle(EventElement):
    game_section = models.CharField(max_length=50, null=True, verbose_name='GameSection')
    final_result = models.CharField(max_length=50, null=True, verbose_name='FinalResult')
    breaking_off = models.CharField(max_length=50, null=True, verbose_name='BreakingOff')


class Offside(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')


class Foul(EventElement):
    team_fouler = models.ForeignKey(MatchTeam, null=True, verbose_name='TeamFouler', related_name='team_fouler+')
    team_fouled = models.ForeignKey(MatchTeam, null=True, verbose_name='TeamFouled', related_name='team_fouled+')
    fouler = models.CharField(max_length=50, null=True, verbose_name='Fouler')
    fouled = models.CharField(max_length=50, null=True, verbose_name='Fouled')
    foul_type = models.CharField(max_length=50, null=True, verbose_name='FoulType')


class TacklingGame(EventElement):
    winner_team = models.ForeignKey(MatchTeam, null=True, verbose_name='WinnerTeam', related_name='winner_team+')
    winner = models.CharField(max_length=50, null=True, verbose_name='Winner')
    loser_team = models.ForeignKey(MatchTeam, null=True, verbose_name='LoserTeam', related_name='loser_team+')
    loser = models.CharField(max_length=50, null=True, verbose_name='Loser')
    goal_keeper_involved = models.CharField(max_length=50, null=True, verbose_name='GoalKeeperInvolved')
    winner_role = models.CharField(max_length=50, null=True, verbose_name='WinnerRole')
    loser_role = models.CharField(max_length=50, null=True, verbose_name='LoserRole')
    winner_result = models.CharField(max_length=50, null=True, verbose_name='WinnerResult')
    type = models.CharField(max_length=50, null=True, verbose_name='Type')
    dribbling = models.CharField(max_length=50, null=True, verbose_name='Dribbling')


class BallContactWithoutControl(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')


class OtherPlayerAction(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    reason = models.CharField(max_length=50, null=True, verbose_name='Reason')
    change_of_captain = models.CharField(max_length=50, null=True, verbose_name='ChangeOfCaptain')
    change_contingent_exhausted = models.CharField(max_length=50, null=True, verbose_name='ChangeContingentExhausted')


class ShotAtGoal(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    type_of_shot = models.CharField(max_length=50, null=True, verbose_name='TypeOfShot')
    shot_origin = models.CharField(max_length=50, null=True, verbose_name='ShotOrigin')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')
    after_free_kick = models.CharField(max_length=50, null=True, verbose_name='AfterFreeKick')


class SuccessfulShot(EventElement):
    assist = models.CharField(max_length=50, null=True, verbose_name='Assist')
    goa = models.CharField(max_length=50, null=True, verbose_name='Goa')
    assist_type = models.CharField(max_length=50, null=True, verbose_name='AssistType')
    goalzone = models.CharField(max_length=50, null=True, verbose_name='Goalzone')
    counter_attack = models.CharField(max_length=50, null=True, verbose_name='CounterAttack')
    current_result = models.CharField(max_length=50, null=True, verbose_name='CurrentResult')


class SavedShot(EventElement):
    goal_keeper = models.ForeignKey(MatchPlayer, null=True, verbose_name='GoalKeeper', related_name='player+')
    save_type = models.CharField(max_length=50, null=True, verbose_name='SaveType')
    save_result = models.CharField(max_length=50, null=True, verbose_name='SaveResult')
    post_touch = models.CharField(max_length=50, null=True, verbose_name='PostTouch')
    goalzone = models.CharField(max_length=50, null=True, verbose_name='Goalzone')


class BlockedShot(EventElement):
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    goal_prevented = models.CharField(max_length=50, null=True, verbose_name='GoalPrevented')
    blocked_by_own_team = models.CharField(max_length=50, null=True, verbose_name='BlockedByOwnTeam')


class ShotWide(EventElement):
    placing = models.CharField(max_length=50, null=True, verbose_name='Placing')
    pitch_marking = models.CharField(max_length=50, null=True, verbose_name='PitchMarking')


class ShotWoodWork(EventElement):
    location = models.CharField(max_length=50, null=True, verbose_name='Location')


class OtherShot(EventElement):
    pass


class Play(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    from_open_play = models.CharField(max_length=50, null=True, verbose_name='FromOpenPlay')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')
    successful = models.CharField(max_length=50, null=True, verbose_name='Successful')
    height = models.CharField(max_length=50, null=True, verbose_name='Height')
    penalty_box = models.CharField(max_length=50, null=True, verbose_name='PenaltyBox')
    distance = models.CharField(max_length=50, null=True, verbose_name='Distance')
    goal_keeper_action = models.CharField(max_length=50, null=True, verbose_name='GoalKeeperAction')
    play_origin = models.CharField(max_length=50, null=True, verbose_name='PlayOrigin')
    pass_origin = models.CharField(max_length=50, null=True, verbose_name='PassOrigin')
    blocked = models.CharField(max_length=50, null=True, verbose_name='Blocked')
    technique = models.CharField(max_length=50, null=True, verbose_name='Technique')


class Pass(EventElement):
    pass_origin = models.CharField(max_length=50, null=True, verbose_name='PassOrigin')
    free_kick_layup = models.CharField(max_length=50, null=True, verbose_name='FreeKickLayup')
    def __str__(self):
        return "Pass"


class Cross(EventElement):
    goal_keeper_interference = models.CharField(max_length=50, null=True, verbose_name='GoalKeeperInterference')
    intercepted = models.CharField(max_length=50, null=True, verbose_name='Intercepted')
    goal_keeper = models.CharField(max_length=50, null=True, verbose_name='GoalKeeper')
    side = models.CharField(max_length=50, null=True, verbose_name='Side')


class OwnGoal(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')
    type_of_shot = models.CharField(max_length=50, null=True, verbose_name='TypeOfShot')
    current_result = models.CharField(max_length=50, null=True, verbose_name='CurrentResult')
    shot_origin = models.CharField(max_length=50, null=True, verbose_name='ShotOrigin')
    goal_zone = models.CharField(max_length=50, null=True, verbose_name='GoalZone')


class PreventedOwnGoal(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')
    save_type = models.CharField(max_length=50, null=True, verbose_name='SaveType')
    save_result = models.CharField(max_length=50, null=True, verbose_name='SaveResult')
    post_touch = models.CharField(max_length=50, null=True, verbose_name='PostTouch')


class DefensiveClearance(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')


class FairPlay(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')


class AbandonmentOfBall(EventElement):
    pass


class OtherBallAction(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')


class OtherBallContact(EventElement):
    pass


class ThrowIn(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    side = models.CharField(max_length=50, null=True, verbose_name='Side')


class FaultExecution(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')


class Penalty(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    fouled_player = models.ForeignKey(MatchPlayer, null=True, verbose_name='FouledPlayer', related_name='fouled_player+')
    causing_player = models.ForeignKey(MatchPlayer, null=True, verbose_name='CausingPlayer', related_name='causing_player+')


class CornerKick(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    side = models.CharField(max_length=50, null=True, verbose_name='Side')
    placing = models.CharField(max_length=50, null=True, verbose_name='Placing')
    rotation = models.CharField(max_length=50, null=True, verbose_name='Rotation')


class FreeKick(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    execution_mode = models.CharField(max_length=50, null=True, verbose_name='ExecutionMode')


class GoalKick(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')



class BallClaiming(EventElement):
    team = models.ForeignKey(MatchTeam, null=True, verbose_name='Team', related_name='team+')
    player = models.ForeignKey(MatchPlayer, null=True, verbose_name='Player', related_name='player+')
    ball_possession_phase = models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')
    type = models.CharField(max_length=50, null=True, verbose_name='Type')


class CounterAttack(EventElement):
    pass


class Kickoff(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')



class KickoffAfterGoal(EventElement):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')



class Delete(EventElement):
    pass
