from django.contrib import admin
from timetrack import models

admin.register(models.Project)
admin.register(models.Task)
admin.register(models.WorkType)
admin.register(models.WorkLog)
admin.register(models.WorkLogHistory)
admin.register(models.Request)
admin.register(models.DayOffLog)
