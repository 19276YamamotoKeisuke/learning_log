from django.contrib import admin

# Register your models here.

from .models import Topic, Entry, Apply
# , UploadImage

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Apply)
# admin.site.register(UploadImage)
