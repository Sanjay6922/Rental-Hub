from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(login)
admin.site.register(veh_listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Contact)

# Register your models here.
