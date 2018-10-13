from django.contrib import admin
from .models import Education, Certification, Language, Resume, Skill, WorkExperience


class ResumeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    search_fields = ['name', ]
    list_filter = ['created_at', ]
    list_display = ['name', 'user', 'created_at', 'updated_at', ]


class WorkExperienceAdmin(admin.ModelAdmin):
    search_fields = ['position', 'company', ]
    list_display = ['position', 'company', 'resume', ]


class EducationAdmin(admin.ModelAdmin):
    search_fields = ['school', ]
    list_display = ['school', 'resume', ]


class CertificationAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['name', 'resume', ]


class SkillAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['name', 'resume', ]


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['name', 'resume', ]


admin.site.register(Resume, ResumeAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Language, LanguageAdmin)
