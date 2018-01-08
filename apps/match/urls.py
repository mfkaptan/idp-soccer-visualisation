from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.MatchList.as_view(),
        name="match_list"),
    url(r'^(?P<pk>[A-Z-0-9]+)/match_detail$',
        views.MatchDetail.as_view(),
        name="match_detail"),
    url(r'^(?P<pk>[A-Z-0-9]+)/ball_possession',
        views.BallPossession.as_view(),
        name="ball_possession"),
]
