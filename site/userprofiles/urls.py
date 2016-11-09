from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required as auth

urlpatterns = [
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^profile/(?P<slug>.*)/$',
        auth(views.UserProfileDetailView.as_view()), name='profile'),
    url(r'^edit-profile/$', auth(views.EditProfile.as_view()), name='editprofile'),
]
