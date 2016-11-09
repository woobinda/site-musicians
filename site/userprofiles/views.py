from django.views.generic import FormView, RedirectView, DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.core.exceptions import PermissionDenied


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'userprofiles/registration.html'

    def get_context_data(self, **kwargs):
        kwargs = super(RegistrationView, self).get_context_data(**kwargs)
        kwargs['title'] = 'Registeration'
        return kwargs

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        form.save()
        url = reverse('userprofiles:login')
        return HttpResponseRedirect(url)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "userprofiles/login.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_context_data(self, **kwargs):
        d = super(LoginView, self).get_context_data(**kwargs)
        d['title'] = 'Login'
        return d

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse("musicians:index")


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = 'userprofiles/user_detail.html'

    def get_context_data(self, **kwargs):
        d = super(UserProfileDetailView, self).get_context_data(**kwargs)
        d['profile'] = UserProfile.objects.get_or_create(
            user=self.request.user)[0]
        d['title'] = 'Profile'
        return d

    def get_object(self, queryset=None, ):
        user = super(UserProfileDetailView, self).get_object(queryset)
        if user != self.request.user:
            raise PermissionDenied
        UserProfile.objects.get_or_create(user=user)
        return user


class EditProfile(UpdateView):
    model = UserProfile
    form_class = EditProfileForm
    template_name = 'userprofiles/edit_profile.html'

    def get_context_data(self, **kwargs):
        kwargs = super(EditProfile, self).get_context_data(**kwargs)
        kwargs['title'] = 'Edit Profile'
        return kwargs

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("userprofiles:profile", kwargs={"slug": self.request.user})
