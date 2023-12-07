from django.contrib import admin

from .models import AdvUser, Machine, Spare

admin.site.register(AdvUser)
admin.site.register(Machine)
admin.site.register(Spare)
