from django.contrib import admin
from .models import Vulnerability, Date

class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ('vul_name', 'severity',)
    # list_display_links = ('vul_name', 'severity',)
    # search_fields = ('vul_name', 'severity',)
    # list_per_page = 25

class DateAdmin(admin.ModelAdmin):
    list_display = ('vuln', 'publish_date',)

admin.site.register(Vulnerability, VulnerabilityAdmin)
admin.site.register(Date, DateAdmin)
