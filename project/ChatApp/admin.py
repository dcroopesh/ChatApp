from django.contrib import admin
from .models import chatapp,p2p,room
# Register your models here.
admin.site.register(chatapp)
admin.site.register(p2p)
admin.site.register(room)