from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.completed)
admin.site.register(models.error)
admin.site.register(models.found_automatic)
admin.site.register(models.last_checked_number)
admin.site.register(models.multi_user)
admin.site.register(models.semi_found)
admin.site.register(models.running_status)
