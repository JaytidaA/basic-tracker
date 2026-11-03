from django.contrib import admin
from .models import Entry, Tracking

# Register your models here.
@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ["name", "kind", "start_date", "end_date", "is_active"]
    list_filter = ["kind", "is_active"]
    filter_horizontal = ["members"]

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["user", "tracking", "value", "occurred_at"]
    list_filter = ["tracking", "user"]
