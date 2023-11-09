from django.contrib import admin

from .models import Bb


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'published')
    list_display_links = ('title',)
    search_fields = ('title', 'content')


admin.site.register(Bb, BbAdmin)
