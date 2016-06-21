from django.db import models

from apps.match.models import Match, MatchTeam, MatchPlayer


class FrameSetManager(models.Manager):
    def get_for_player(self, player, min):
        if half == 0:
            return FrameSet.objects.filter(player_id=player)
        else:
            half = "firstHalf" if half == 1 else "secondHalf"
            return FrameSet.objects.filter(player_id=player, half=half)


class FrameSet(models.Model):
    game_section = models.CharField(max_length=20, null=True)

    match = models.ForeignKey(Match, null=True)
    team = models.ForeignKey(MatchTeam, null=True)
    player = models.ForeignKey(MatchPlayer, null=True)

    objects = FrameSetManager()

    class Meta:
        verbose_name = "FrameSet"
        verbose_name_plural = "FrameSets"

    def __str__(self):
        try:
            if self.player:
                return self.game_section + " " + str(self.player)
            else:
                return "Ball"
        except:
            return "Ball"


class Frame(models.Model):
    n = models.IntegerField(null=True, verbose_name="N")
    t = models.DateTimeField(null=True, verbose_name="T")
    x = models.FloatField(null=True, verbose_name="X")
    y = models.FloatField(null=True, verbose_name="Y")
    z = models.FloatField(null=True, verbose_name="Z")
    s = models.FloatField(null=True, verbose_name="S")
    m = models.IntegerField(null=True, verbose_name="M")
    ball_posession = models.IntegerField(null=True, verbose_name="BallPossession")
    ball_status = models.IntegerField(null=True, verbose_name="BallStatus")

    set = models.ForeignKey(FrameSet, null=True, verbose_name="FrameSet")

    class Meta:
        verbose_name = "Frame"
        verbose_name_plural = "Frames"

    def __str__(self):
        return "Min: " + str(self.m) + " " + str(self.set)

