from django.http import HttpResponse
from django.views.generic import ListView

from .models import Match

# Create your views here.

class MatchList(ListView):
    model = Match

