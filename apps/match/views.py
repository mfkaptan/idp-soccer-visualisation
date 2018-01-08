from django.views.generic import ListView, DetailView

from .models import Match


class MatchList(ListView):
    model = Match


class MatchDetail(DetailView):
    model = Match


class BallPossession(DetailView):
    model = Match
    template_name = "match/ball_possession.html"
