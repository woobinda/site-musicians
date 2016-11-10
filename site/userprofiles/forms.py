from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(forms.Form):
    username = forms.RegexField(label="*  Username", max_length=30, min_length=5,
                                regex=r'^[\w.-]+$',
                                error_messages={
                                    'invalid': 'Contain only letters, numbers and ./-/_ characters.'})
    email = forms.EmailField(label='*  E-mail')
    password = forms.CharField(label='*  Password', min_length=8,
                               widget=forms.PasswordInput(render_value=False))
    location = forms.CharField(label='Location', required=False)
    age = forms.IntegerField(required=False)
    GENDER_CHOICES = (
        ('-----', '-----'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Enter Your User Name'})

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'example@company.com'})

        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Easy to remember, hard to guess'})

        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'placeholder': 'Your Age'})

        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update(
            {'placeholder': 'Location'})

        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'placeholder': 'Gender'})

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            user = User.objects.get(username=data)
        except Exception:
            return data
        else:
            raise forms.ValidationError(
                "Sorry, but this username is already in use")

    def save(self, *args, **kwargs):
        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        new_user.userprofile.age = self.cleaned_data['age']
        new_user.userprofile.location = self.cleaned_data['location']
        new_user.userprofile.gender = self.cleaned_data['gender']
        new_user.userprofile.save()

        if hasattr(self, 'save_profile'):
            self.save_profile(new_user, *args, **kwargs)

        return new_user


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'Your First Name'})

        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Your Last Name'})

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail'})


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.user_form = UserForm(*args, **user_kwargs)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.user_form.fields)
        self.initial.update(self.user_form.initial)

        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'placeholder': 'Your Age'})

        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update(
            {'placeholder': 'Location'})

        self.fields['profile_picture'].widget.attrs.update(
            {'class': 'form-control-static'})
        self.fields['profile_picture'].widget.attrs.update(
            {'placeholder': 'Avatar img'})

        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'placeholder': 'Gender'})

        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'placeholder': 'Company'})

        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update(
            {'placeholder': 'http://example.com'})

    def save(self, *args, **kwargs):
        self.user_form.save(*args, **kwargs)
        return super(EditProfileForm, self).save(*args, **kwargs)
