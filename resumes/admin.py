from django.contrib import admin
from .models import Resume, WorkExperience, Education


class ResumeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class WorkExperienceAdmin(admin.ModelAdmin):
    pass


class EducationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Resume, ResumeAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Education, EducationAdmin)
