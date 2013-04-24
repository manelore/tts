from django.contrib import admin
from timetrack import models

admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.WorkType)
admin.site.register(models.WorkLog)
admin.site.register(models.WorkLogHistory)
admin.site.register(models.Request)
admin.site.register(models.DayOffLog)
