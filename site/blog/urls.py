from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.blog_view, name='index'),
    url(r'^category/(?P<categoryslug>[-\w]*)/$',
        views.blog_view, name='blog_by_category'),
    url(r'^tag/(?P<tagslug>[-\w]*)/$', views.blog_view, name='blog_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]*)/$',
        views.ArticleDetail.as_view(), name='article_detail'),
]
