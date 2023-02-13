from django.contrib import admin
# Register your models here.

from .models import Topic, Entry, Apply, Profile, User, Recommend
# , UploadImage

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Apply)
admin.site.register(Recommend)
# admin.site.register(User)
admin.site.register(Profile)
# admin.site.register(UploadImage)
