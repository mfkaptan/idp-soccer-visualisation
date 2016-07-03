from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>[A-Z-0-9]+)/get_data/(?P<half>[0-9]+)/(?P<minute>[0-9]+)$',
        views.get_data,
        name="get_data"),
]
