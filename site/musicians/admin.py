from django.contrib import admin
from .models import Musician, MusicStyle, MusicianInstrument, VideoUrl


class MusicianAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'playing_style', 'created_date', )
    readonly_fields = ('created_date',)
    list_display_links = ('full_name',)
    prepopulated_fields = {"slug": ("first_name", "last_name")}

admin.site.register(Musician, MusicianAdmin)


class MusicStyleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",), }

admin.site.register(MusicStyle, MusicStyleAdmin)


class MusicianInstrumentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(MusicianInstrument, MusicianInstrumentAdmin)
admin.site.register(VideoUrl)
