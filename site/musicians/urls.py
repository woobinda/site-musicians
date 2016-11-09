from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required as auth

urlpatterns = [
    url(r'^$', views.musicians_view, name='index'),
    url(r'^playingstyle/(?P<playingstyleslug>[-\w]*)/$',
        views.musicians_view, name='musicians_by_playing_style'),
    url(r'^instrument/(?P<instrumentslug>[-\w]*)/$',
        views.musicians_view, name='musicians_by_instrument'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]*)/$',
        views.MusicianDetail.as_view(), name='musician_detail'),
    url(r'^add-musician/$', auth(views.AddMusician.as_view()), name='add_musician'),
    url(r'^add-video/(?P<slug>[-\w]*)/$',
        auth(views.AddVideo.as_view()), name='add_video'),
]
