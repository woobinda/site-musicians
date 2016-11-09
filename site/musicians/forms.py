from django import forms
from .models import Musician, VideoUrl


class MusicianForm(forms.ModelForm):

    class Meta:
        model = Musician
        fields = '__all__'
        exclude = ['slug', 'instrument_slug', 'playing_style_slug', 'owner']

    def __init__(self, *args, **kwargs):
        super(MusicianForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'about_you':
                self.fields[field].widget.attrs.update(
                    {'placeholder': 'Some information about you'})
            if field == 'avatar':
                self.fields[field].widget.attrs[
                    'class'] = 'form-control-static'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        new_musician = super(MusicianForm, self).save(commit=True)
        return new_musician


class AddVideoForm(forms.ModelForm):

    class Meta:
        model = VideoUrl
        fields = '__all__'
        exclude = ['host', ]

    def __init__(self, *args, **kwargs):
        super(AddVideoForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'name':
                self.fields[field].widget.attrs['class'] = 'form-control'
                self.fields[field].widget.attrs.update(
                    {'placeholder': 'Name for this video'})
            if field == 'url':
                self.fields[field].widget.attrs['class'] = 'form-control'
                self.fields[field].widget.attrs.update(
                    {'placeholder': 'https://youtube/example'})
