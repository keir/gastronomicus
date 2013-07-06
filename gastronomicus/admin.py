from django.contrib import admin
from models import Meeting
from models import Dish
from models import Serving
from models import Attendee

admin.site.register(Meeting)
admin.site.register(Dish)
admin.site.register(Serving)
admin.site.register(Attendee)
