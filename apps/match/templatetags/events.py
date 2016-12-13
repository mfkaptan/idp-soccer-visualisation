from django.template import Library
from django.utils.safestring import mark_safe

from rest_framework.renderers import JSONRenderer

from apps.event.serializers import ShotEventSerializer, FoulEventSerializer


register = Library()


@register.filter(name="shots", is_safe=True)
def shots(match):
    serializer = ShotEventSerializer(match.get_shots, many=True)
    return mark_safe(JSONRenderer().render(serializer.data))


@register.filter(name="fouls", is_safe=True)
def fouls(match):
    serializer = FoulEventSerializer(match.get_fouls, many=True)
    return mark_safe(JSONRenderer().render(serializer.data))