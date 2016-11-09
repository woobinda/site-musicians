from django.shortcuts import render
from .models import Musician, MusicStyle, MusicianInstrument, VideoUrl
from django.views.generic import FormView, DetailView, CreateView
from django.core.urlresolvers import reverse
from .forms import MusicianForm, AddVideoForm

style_list = MusicStyle.objects.all()
instrument_list = MusicianInstrument.objects.all()


def musicians_view(request, instrumentslug=None, playingstyleslug=None):
    musicians_list = Musician.objects.order_by('-created_date')
    title = 'Musicians'

    if playingstyleslug:
        musicians_list = musicians_list.filter(
            playing_style__slug=playingstyleslug)
        title = MusicStyle.objects.get(slug=playingstyleslug)

    if instrumentslug:
        musicians_list = musicians_list.filter(instrument__slug=instrumentslug)
        title = MusicianInstrument.objects.get(slug=instrumentslug)

    def count(count=0):
        for musician in musicians_list:
            if musician:
                count += 1
        return count

    return render(request, 'musicians/musicians_index.html', {'musicians': musicians_list,
                                                              'title': title,
                                                              'style_list': style_list,
                                                              'instrument_list': instrument_list,
                                                              'count': count()})


class MusicianDetail(DetailView):
    model = Musician
    template_name = 'musicians/musician_detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super(MusicianDetail, self).get_context_data(**kwargs)
        musician = self.get_object()
        instrument = musician.instrument
        playing_style = musician.playing_style
        ids = musician.id
        video_urls = VideoUrl.objects.filter(host=musician)
        kwargs['musician'] = musician
        kwargs['video_urls'] = video_urls
        kwargs['style_list'] = style_list
        kwargs['instrument_list'] = instrument_list
        kwargs['title'] = musician
        kwargs['similar_musicians'] = Musician.objects.filter(instrument=instrument,
                                                              playing_style=playing_style).exclude(id=ids)[:4]
        return kwargs


class AddMusician(FormView):
    template_name = 'musicians/add_musician.html'
    form_class = MusicianForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super(AddMusician, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs = super(AddMusician, self).get_context_data(**kwargs)
        kwargs['title'] = 'Add Musician'
        kwargs['style_list'] = style_list
        kwargs['instrument_list'] = instrument_list
        return kwargs

    def get_success_url(self):
        return reverse("musicians:index")


class AddVideo(CreateView):
    template_name = 'musicians/add_video.html'
    form_class = AddVideoForm
    model = Musician

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.host = self.get_object()
        instance.save()
        return super(AddVideo, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs = super(AddVideo, self).get_context_data(**kwargs)
        kwargs['musician'] = self.get_object()
        kwargs['title'] = 'Add Video'
        kwargs['style_list'] = style_list
        kwargs['instrument_list'] = instrument_list
        return kwargs

    def get_success_url(self):
        return self.get_object().get_absolute_url()
