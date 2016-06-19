from django.conf.urls import url

from .views import MatchList

urlpatterns = [
    url(r'^$', MatchList.as_view()),
]
