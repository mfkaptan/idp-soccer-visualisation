from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .serializers import FrameSerializer, FrameSetSerializer
from .. import models


class FrameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FrameSerializer
    queryset = models.Frame.objects.order_by('n')

    @detail_route()
    def home_players(self, request, pk=None):
        frames = self.queryset.filter(set__match_id=pk, set__team__role='home')
        return Response(FrameSerializer(frames, many=True).data)

    @detail_route()
    def min(self, request, pk=None):
        frames = self.queryset.filter(m=int(pk))
        serializer = FrameSerializer(frames, many=True)
        return Response(serializer.data)

    @detail_route()
    def set(self, request, pk=None):
        frames = self.queryset.filter(set_id=int(pk))
        serializer = FrameSerializer(frames, many=True)
        return Response(serializer.data)


class FrameSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.FrameSet.objects.all()
    serializer_class = FrameSetSerializer

    @detail_route()
    def first_half(self, request, pk=None):
        fset = self.queryset.filter(match_id=pk, game_section="firstHalf")
        return Response(FrameSetSerializer(fset, many=True).data)

    @detail_route()
    def second_half(self, request, pk=None):
        fset = self.queryset.filter(match_id=pk, game_section="secondHalf")
        return Response(FrameSetSerializer(fset, many=True).data)
