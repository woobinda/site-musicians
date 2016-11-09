"""newsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from home import views
from django.views.generic.base import RedirectView, TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'favicon.ico'), name='favicon.ico'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots.txt'),
]

urlpatterns += [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^musicians/', include('musicians.urls', namespace="musicians")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^userprofiles/', include('userprofiles.urls', namespace="userprofiles")),
    url(r'^shop/', include('shop.urls', namespace="shop")),
    url(r'^cart/', include('cart.urls', namespace="cart")),
    url(r'^coupons/', include('coupons.urls', namespace="coupons")),
    url(r'^order/', include('order.urls', namespace="order")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
