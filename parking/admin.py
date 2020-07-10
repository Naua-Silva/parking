from django.contrib import admin
from .models import *

@admin.register(Reserve)

class ReserveAdmin(admin.ModelAdmin):
	list_display = ['id', 'plate', 'entryTime', 'departureTime', 'time', 'In', 'paid']
