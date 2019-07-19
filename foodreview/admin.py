from django.contrib import admin

from .models import *

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Region)
admin.site.register(ReviewInstance)