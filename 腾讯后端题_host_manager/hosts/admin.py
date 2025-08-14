from django.contrib import admin
from .models import City, IDC, Host, HostStats


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(IDC)
class IDCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostname', 'ip', 'city', 'idc', 'ping_last_ok', 'ping_last_rtt_ms', 'password_updated_at')
    list_filter = ('city', 'idc', 'ping_last_ok')
    search_fields = ('hostname', 'ip')


@admin.register(HostStats)
class HostStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'stat_date', 'city', 'idc', 'host_count')
    list_filter = ('stat_date', 'city', 'idc')
