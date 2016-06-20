from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

from .models import Match

# Create your views here.

class MatchList(ListView):
    model = Match


class MatchDetail(TemplateView):
    template_name = "match/match_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MatchDetail, self).get_context_data(**kwargs)

        context["match"] = Match.objects.get(pk=kwargs["pk"])
        return context
