from django.contrib import admin

# Register your models here.
from .models import WebhookEvent,Profile

class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'reference_id', 'status', 'received_at')
    search_fields = ('event_type', 'reference_id', 'status')
    list_filter = ('event_type', 'status')
    ordering = ('-received_at',)
    readonly_fields = ('event_type', 'reference_id', 'status', 'received_at')
    actions = ['mark_as_processed']
    def mark_as_processed(self, request, queryset):
        for event in queryset:
            event.status = 'processed'
            event.save()
        self.message_user(request, f"{queryset.count()} events marked as processed.")
    fieldsets = (
        ('Event Info', {
            'fields': ('event_type', 'reference_id')
        }),
        ('Status Info', {
            'fields': ('status', 'received_at'),
            'classes': ('collapse',),
        }),
    )


admin.site.register(WebhookEvent,WebhookEventAdmin)
admin.site.register(Profile)

