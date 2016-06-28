from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from . import serializers
from .. import models


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer

    def retrieve(self, request, pk=None):
        return Response(serializers.MatchDetailSerializer(self.get_object()).data)

    @detail_route()
    def teams(self, request, pk=None):
        teams = self.get_object().matchteam_set.all()
        return Response(serializers.MatchTeamSerializer(teams, many=True).data)

    @detail_route()
    def home_team(self, request, pk=None):
        home_team = self.get_object().home_team
        return Response(serializers.MatchTeamSerializer(home_team).data)

    @detail_route()
    def away_team(self, request, pk=None):
        away_team = self.get_object().away_team
        return Response(serializers.MatchTeamSerializer(away_team).data)
