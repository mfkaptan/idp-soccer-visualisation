from lxml import etree

from django.core.management.base import BaseCommand, CommandError

from apps.posdata.models import *


class Command(BaseCommand):
    help = 'Imports given position data xml to database'
    FRAME_COUNT = 0
    FRAME_SET_COUNT = 0
    match = None
    teams = None
    players = None

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('match', type=str)

    def process_frame(self, frameset, e):
        frame = Frame()
        frame.n = int(e.get("N"))
        frame.t = e.get("T")
        frame.m = int(e.get("M"))
        frame.s = float(e.get("S"))
        frame.x = float(e.get("X"))
        frame.y = float(e.get("Y"))
        try:
            frame.z = float(e.get("Z"))
            frame.ball_posession = int(e.get("BallPossession"))
            frame.ball_status = int(e.get("BallStatus"))
        except:
            pass

        frame.set = frameset

        self.FRAME_COUNT += 1

        return frame

    def process_frameset(self, e):
        frameset = FrameSet()

        frameset.game_section = e.get("GameSection")
        frameset.match_id = self.match
        frameset.team = self.teams[e.get("TeamId")]
        try:
            p = self.players[e.get("PersonId")]
        except:
            p = None
        frameset.player = p

        frameset.save()

        self.FRAME_SET_COUNT += 1
        print("FrameSet done: ", self.FRAME_SET_COUNT)

        return frameset

    def fast_iter_frame(self, frameset, context):
        flist = []
        for elem in context.iterfind("Frame"):
            flist.append(self.process_frame(frameset, elem))
            elem.clear()
            for ancestor in elem.xpath('ancestor-or-self::*'):
                #print('Checking ancestor: {a}'.format(a=ancestor.tag))
                while ancestor.getprevious() is not None:
                    #print('Deleting {p}'.format(p=(ancestor.getparent()[0]).tag))
                    del ancestor.getparent()[0]
        Frame.objects.bulk_create(flist)
        print(len(flist), " frames imported")
        del flist
        del context

    def fast_iter_frameset(self, context):
        for elem in context.iterfind("FrameSet"):
            frameset = self.process_frameset(elem)
            self.fast_iter_frame(frameset, elem)
            elem.clear()

            for ancestor in elem.xpath('ancestor-or-self::*'):
                #print('Checking ancestor: {a}'.format(a=ancestor.tag))
                while ancestor.getprevious() is not None:
                    #print('Deleting {p}'.format(p=(ancestor.getparent()[0]).tag))
                    del ancestor.getparent()[0]

        del context

    def handle(self, *args, **options):
        self.match = options['match']
        self.teams = {t.team.team_id: t for t in MatchTeam.objects.filter(match__match_id=self.match)}
        self.teams["Ball"] = None
        self.players = {p.player.player_id: p for p in MatchPlayer.objects.filter(match_team__match__match_id=self.match)}
        print("Starting to parse")
        print(self.match)
        print(self.teams)
        print(self.players)
        context = etree.parse(options['file'])
        print("Parsing finished, importing data.")
        print("This will take a while...")
        self.fast_iter_frameset(context.getroot().getchildren()[0])

        print(self.FRAME_SET_COUNT, " frame sets imported")
        print(self.FRAME_COUNT, " frames imported")
