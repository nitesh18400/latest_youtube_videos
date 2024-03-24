from django.contrib import admin

from video_service.models import Video, GoogleAPIClientKey

models = [Video, GoogleAPIClientKey]

for model in models:
    admin.site.register(model)


