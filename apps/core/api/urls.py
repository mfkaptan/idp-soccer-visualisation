from rest_framework import routers

from apps.match.api import view_sets as match_view_sets
from apps.posdata.api import view_sets as posdata_view_sets


router = routers.DefaultRouter()

router.register(r'matches', match_view_sets.MatchViewSet,
                base_name='matches')

router.register(r'framesets', posdata_view_sets.FrameSetViewSet,
                base_name='framesets')

# router.register(r'frames/(?P<project_pk>[0-9]+)/bla', posdata_view_sets.FrameBlaViewSet,
#                 base_name='frames-bla')
router.register(r'frames', posdata_view_sets.FrameViewSet,
                base_name='frames')
