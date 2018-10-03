from django.contrib import admin
from .models import Resume


class ResumeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Resume, ResumeAdmin)
