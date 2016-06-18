# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-18 00:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('match', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbandonmentOfBall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BallClaiming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('type', models.CharField(max_length=50, null=True, verbose_name='Type')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BallContactWithoutControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockedShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_prevented', models.CharField(max_length=50, null=True, verbose_name='GoalPrevented')),
                ('blocked_by_own_team', models.CharField(max_length=50, null=True, verbose_name='BlockedByOwnTeam')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Caution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_color', models.CharField(max_length=50, null=True, verbose_name='CardColor')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CornerKick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('side', models.CharField(max_length=50, null=True, verbose_name='Side')),
                ('placing', models.CharField(max_length=50, null=True, verbose_name='Placing')),
                ('rotation', models.CharField(max_length=50, null=True, verbose_name='Rotation')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CounterAttack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cross',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_keeper_interference', models.CharField(max_length=50, null=True, verbose_name='GoalKeeperInterference')),
                ('intercepted', models.CharField(max_length=50, null=True, verbose_name='Intercepted')),
                ('goal_keeper', models.CharField(max_length=50, null=True, verbose_name='GoalKeeper')),
                ('side', models.CharField(max_length=50, null=True, verbose_name='Side')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefensiveClearance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Delete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='EventId')),
                ('time', models.DateTimeField(null=True, verbose_name='EventTime')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.Match')),
            ],
        ),
        migrations.CreateModel(
            name='FairPlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FaultExecution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FinalWhistle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_section', models.CharField(max_length=50, null=True, verbose_name='GameSection')),
                ('final_result', models.CharField(max_length=50, null=True, verbose_name='FinalResult')),
                ('breaking_off', models.CharField(max_length=50, null=True, verbose_name='BreakingOff')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Foul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fouler', models.CharField(max_length=50, null=True, verbose_name='Fouler')),
                ('fouled', models.CharField(max_length=50, null=True, verbose_name='Fouled')),
                ('foul_type', models.CharField(max_length=50, null=True, verbose_name='FoulType')),
                ('team_fouled', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_fouled+', to='match.MatchTeam', verbose_name='TeamFouled')),
                ('team_fouler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_fouler+', to='match.MatchTeam', verbose_name='TeamFouler')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FreeKick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('execution_mode', models.CharField(max_length=50, null=True, verbose_name='ExecutionMode')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GoalKick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Kickoff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KickoffAfterGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KickoffWhistle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_section', models.CharField(max_length=50, null=True, verbose_name='GameSection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Offside',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherBallAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherBallContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherPlayerAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50, null=True, verbose_name='Reason')),
                ('change_of_captain', models.CharField(max_length=50, null=True, verbose_name='ChangeOfCaptain')),
                ('change_contingent_exhausted', models.CharField(max_length=50, null=True, verbose_name='ChangeContingentExhausted')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherRefereeAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50, null=True, verbose_name='Reason')),
                ('start_time', models.DateTimeField(null=True, verbose_name='StartTime')),
                ('end_time', models.DateTimeField(null=True, verbose_name='EndTime')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OwnGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('type_of_shot', models.CharField(max_length=50, null=True, verbose_name='TypeOfShot')),
                ('current_result', models.CharField(max_length=50, null=True, verbose_name='CurrentResult')),
                ('shot_origin', models.CharField(max_length=50, null=True, verbose_name='ShotOrigin')),
                ('goal_zone', models.CharField(max_length=50, null=True, verbose_name='GoalZone')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_origin', models.CharField(max_length=50, null=True, verbose_name='PassOrigin')),
                ('free_kick_layup', models.CharField(max_length=50, null=True, verbose_name='FreeKickLayup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('causing_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='causing_player+', to='match.MatchPlayer', verbose_name='CausingPlayer')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('fouled_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fouled_player+', to='match.MatchPlayer', verbose_name='FouledPlayer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('from_open_play', models.CharField(max_length=50, null=True, verbose_name='FromOpenPlay')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('successful', models.CharField(max_length=50, null=True, verbose_name='Successful')),
                ('height', models.CharField(max_length=50, null=True, verbose_name='Height')),
                ('penalty_box', models.CharField(max_length=50, null=True, verbose_name='PenaltyBox')),
                ('distance', models.CharField(max_length=50, null=True, verbose_name='Distance')),
                ('goal_keeper_action', models.CharField(max_length=50, null=True, verbose_name='GoalKeeperAction')),
                ('play_origin', models.CharField(max_length=50, null=True, verbose_name='PlayOrigin')),
                ('pass_origin', models.CharField(max_length=50, null=True, verbose_name='PassOrigin')),
                ('blocked', models.CharField(max_length=50, null=True, verbose_name='Blocked')),
                ('technique', models.CharField(max_length=50, null=True, verbose_name='Technique')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PreventedOwnGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('save_type', models.CharField(max_length=50, null=True, verbose_name='SaveType')),
                ('save_result', models.CharField(max_length=50, null=True, verbose_name='SaveResult')),
                ('post_touch', models.CharField(max_length=50, null=True, verbose_name='PostTouch')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RefereeBall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RefereeSubstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referee_in', models.CharField(max_length=50, null=True, verbose_name='RefereeIn')),
                ('referee_out', models.CharField(max_length=50, null=True, verbose_name='RefereeOut')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SavedShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_type', models.CharField(max_length=50, null=True, verbose_name='SaveType')),
                ('save_result', models.CharField(max_length=50, null=True, verbose_name='SaveResult')),
                ('post_touch', models.CharField(max_length=50, null=True, verbose_name='PostTouch')),
                ('goalzone', models.CharField(max_length=50, null=True, verbose_name='Goalzone')),
                ('goal_keeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='GoalKeeper')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SendingOff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShotAtGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('type_of_shot', models.CharField(max_length=50, null=True, verbose_name='TypeOfShot')),
                ('shot_origin', models.CharField(max_length=50, null=True, verbose_name='ShotOrigin')),
                ('ball_possession_phase', models.CharField(max_length=50, null=True, verbose_name='BallPossessionPhase')),
                ('after_free_kick', models.CharField(max_length=50, null=True, verbose_name='AfterFreeKick')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player+', to='match.MatchPlayer', verbose_name='Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShotWide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placing', models.CharField(max_length=50, null=True, verbose_name='Placing')),
                ('pitch_marking', models.CharField(max_length=50, null=True, verbose_name='PitchMarking')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShotWoodWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50, null=True, verbose_name='Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playing_position', models.CharField(max_length=50, null=True, verbose_name='PlayingPosition')),
                ('player_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_in+', to='match.MatchPlayer', verbose_name='PlayerIn')),
                ('player_out', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_out+', to='match.MatchPlayer', verbose_name='PlayerOut')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team+', to='match.MatchTeam', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuccessfulShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assist', models.CharField(max_length=50, null=True, verbose_name='Assist')),
                ('goa', models.CharField(max_length=50, null=True, verbose_name='Goa')),
                ('assist_type', models.CharField(max_length=50, null=True, verbose_name='AssistType')),
                ('goalzone', models.CharField(max_length=50, null=True, verbose_name='Goalzone')),
                ('counter_attack', models.CharField(max_length=50, null=True, verbose_name='CounterAttack')),
                ('current_result', models.CharField(max_length=50, null=True, verbose_name='CurrentResult')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TacklingGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.CharField(max_length=50, null=True, verbose_name='Winner')),
                ('loser', models.CharField(max_length=50, null=True, verbose_name='Loser')),
                ('goal_keeper_involved', models.CharField(max_length=50, null=True, verbose_name='GoalKeeperInvolved')),
                ('winner_role', models.CharField(max_length=50, null=True, verbose_name='WinnerRole')),
                ('loser_role', models.CharField(max_length=50, null=True, verbose_name='LoserRole')),
                ('winner_result', models.CharField(max_length=50, null=True, verbose_name='WinnerResult')),
                ('type', models.CharField(max_length=50, null=True, verbose_name='Type')),
                ('dribbling', models.CharField(max_length=50, null=True, verbose_name='Dribbling')),
                ('loser_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loser_team+', to='match.MatchTeam', verbose_name='LoserTeam')),
                ('winner_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner_team+', to='match.MatchTeam', verbose_name='WinnerTeam')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThrowIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('side', models.CharField(max_length=50, null=True, verbose_name='Side')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
