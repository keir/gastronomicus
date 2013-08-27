from django.contrib import admin
from models import Meeting
from models import Dish
from models import Serving
from models import Attendee

class ServingInline(admin.TabularInline):
    model = Serving
    extra = 1

class MeetingAdmin(admin.ModelAdmin):
    inlines = (ServingInline,)

class DishAdmin(admin.ModelAdmin):
    inlines = (ServingInline,)

class AttendeeAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'notes']

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Serving)
admin.site.register(Attendee, AttendeeAdmin)
