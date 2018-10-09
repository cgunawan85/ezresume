from django.contrib import admin
from .models import Education, Certification, Language, Resume, Skill, WorkExperience


class ResumeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class WorkExperienceAdmin(admin.ModelAdmin):
    pass


class EducationAdmin(admin.ModelAdmin):
    pass


class CertificationAdmin(admin.ModelAdmin):
    pass


class SkillAdmin(admin.ModelAdmin):
    pass


class LanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Resume, ResumeAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Language, LanguageAdmin)
