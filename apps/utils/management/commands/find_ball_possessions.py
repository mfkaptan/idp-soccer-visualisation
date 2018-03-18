import json

from django.core.management.base import BaseCommand
from django.db.models import F

from apps.posdata.models import Frame


class Command(BaseCommand):
    help = 'Finds ball possessions'

    def add_arguments(self, parser):
        parser.add_argument('id', type=str)
        parser.add_argument('grid_size', type=int)

    def handle(self, *args, **options):
        match_id = options.get("id", "DFL-MAT-0025I9")
        grid_size = options.get("grid_size", 3)

        frames = Frame.objects.annotate(sec=F('n') % 25).filter(set__match_id=match_id,
                                                                set__game_section="firstHalf",
                                                                sec=0).order_by("n")
        ball_frames = frames.filter(set__player=None, set__game_section="firstHalf", z__lte=2)
        frames = frames.exclude(set__player=None)

        field = {}

        for b in ball_frames:
            candidates = frames.filter(n=b.n, x__gte=b.x-2, x__lte=b.x+2, y__gte=b.y-2, y__lte=b.y+2)
            for c in candidates:
                shirt_no = c.set.player.shirt_number
                g = self._find_grid(grid_size, c.x, c.y)
                if g < 0:
                    continue
                if shirt_no in field:
                    field[shirt_no][g] = field[shirt_no].get(g, 0) + 1
                else:
                    field[shirt_no] = {g: 1}

        filename = str(frames.first().set.match.pk) + "_bp_gs%d.json" % grid_size
        with open(filename, "w") as outfile:
            json.dump(field, outfile, separators=(',', ':'))


    def _find_grid(self, grid_size, x, y):
        fx = 105 // grid_size  # x grids
        gx = (x + 105/2) / grid_size
        gy = (y + 68/2) / grid_size

        return int(gy * fx + gx)
