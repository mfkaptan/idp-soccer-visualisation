import re
import json
from lxml import etree
from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError

from apps.event.models import *
from apps.match.models import MatchPlayer, MatchTeam


class Command(BaseCommand):
    help = 'Imports given event xml to database'
    OBJ_COUNT = 0

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def object_from_elem(self, obj, e):
        d = {}
        # Get {f.verbose_name: f.name}
        for f in obj._meta.get_fields():
            if not f.many_to_one and f.related_model is None:
                d[f.verbose_name] = f.name
            elif f.many_to_one and f.related_model is not None and f.name != 'content':
                try:
                    if isinstance(f.related_model(), MatchTeam):
                        setattr(obj, f.name, f.related_model.objects.get(team__team_id=e.get(f.verbose_name)))
                    elif isinstance(f.related_model(), MatchPlayer):
                        setattr(obj, f.name, f.related_model.objects.get(player__player_id=e.get(f.verbose_name)))
                except:
                    pass

        for tag in e.keys():
            if tag in d and hasattr(obj, d[tag]):
                setattr(obj, d[tag], e.get(tag))

    def recursive_process(self, e):
        e = e.getchildren()[0]
        obj = eval(e.tag)()
        self.object_from_elem(obj, e)

        if len(e.getchildren()) > 0 and hasattr(obj, "content_object"):
            obj.content_object = self.recursive_process(e)

        obj.save()
        return obj

    def process(self, e):
        event = Event()
        event.event_id = e.get("EventId")
        event.time = e.get("EventTime")
        event.match_id = e.get("MatchId")

        event.content_object = self.recursive_process(e)
        event.save()
        self.OBJ_COUNT += 1

    def fast_iter(self, context):
        for elem in context.iterfind("Event"):
            self.process(elem)
            elem.clear()

            for ancestor in elem.xpath('ancestor-or-self::*'):
                #print('Checking ancestor: {a}'.format(a=ancestor.tag))
                while ancestor.getprevious() is not None:
                    #print('Deleting {p}'.format(p=(ancestor.getparent()[0]).tag))
                    del ancestor.getparent()[0]
        del context

    def handle(self, *args, **options):
        context = etree.parse(options['file'])
        self.fast_iter(context)
        print(self.OBJ_COUNT, " events imported.")

