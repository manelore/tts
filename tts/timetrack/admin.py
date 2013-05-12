from django.contrib import admin
from timetrack import models


class UserProjectInline(admin.TabularInline):
	model = models.UserProject
	extra = 1


class ProjectAdmin(admin.ModelAdmin):
	model = models.Project
	inlines = (UserProjectInline,)


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task)
admin.site.register(models.WorkType)
admin.site.register(models.WorkLog)
admin.site.register(models.WorkLogHistory)
admin.site.register(models.Request)
admin.site.register(models.DayOffLog)
