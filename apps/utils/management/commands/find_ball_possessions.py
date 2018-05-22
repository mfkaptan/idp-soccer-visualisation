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
                                                                sec=0).order_by("n")
        ball_frames = frames.filter(set__player=None, z__lte=2)
        frames = frames.exclude(set__player=None)

        field = {}

        # First half
        field = self.handle_half(field, ball_frames, frames, "firstHalf", grid_size)

        # Second half
        field = self.handle_half(field, ball_frames, frames, "secondHalf", grid_size)

        for i in field:
            if "firstHalf" not in field[i]:
                field[i]["fullMatch"] = field[i]["secondHalf"]
            elif "secondHalf" not in field[i]:
                field[i]["fullMatch"] = field[i]["firstHalf"]
            else:
                f, s = field[i]["firstHalf"], field[i]["secondHalf"]
                field[i]["fullMatch"] = {k: f.get(k, 0) + s.get(k, 0) for k in set(f) | set(s)}

        filename = str(frames.first().set.match.pk) + "_bp_gs%d.json" % grid_size
        with open(filename, "w") as outfile:
            json.dump(field, outfile, separators=(',', ':'))

    def handle_half(self, field, ball_frames, frames, half_name, grid_size):
        ball_frames = ball_frames.filter(set__game_section=half_name)
        half = frames.filter(set__game_section=half_name)

        for b in ball_frames:
            candidates = half.filter(n=b.n, x__gte=b.x-grid_size/2, x__lte=b.x+grid_size/2,
                                     y__gte=b.y-grid_size/2, y__lte=b.y+grid_size/2)
            for c in candidates:
                shirt_no = c.set.player.shirt_number
                side = "home" if c.set.team.role == "home" else "away"
                key = side + str(shirt_no)
                g = self._find_grid(grid_size, c.x, c.y)
                if g < 0:
                    continue
                if key in field and half_name in field[key]:
                    field[key][half_name][g] = field[key][half_name].get(g, 0) + 1
                elif key not in field:
                    field[key] = {half_name: {g: 1}}
                else:
                    field[key][half_name] = {g: 1}

        return field

    def _find_grid(self, grid_size, x, y):
        fx = 105 // grid_size  # x grids
        gx = int((x + 105/2) // grid_size)
        gy = int((y + 68/2) // grid_size)

        return int(gy * fx + gx)
