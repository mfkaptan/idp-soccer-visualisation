from django.views.generic import ListView, DetailView

from .models import Match


class MatchList(ListView):
    model = Match


class MatchDetail(DetailView):
    model = Match
