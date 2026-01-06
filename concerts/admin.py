# concerts/admin.py
from django.contrib import admin
from .models import Venue, Concert, Composition

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "city")

class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 0
    fields = ("order", "composer", "title")
    ordering = ("order",)

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display  = ("title", "date_start", "venue", "is_public")
    list_filter   = ("is_public", "venue", "date_start")
    search_fields = ("title", "venue__name")
    date_hierarchy = "date_start"
    ordering = ("-date_start",)
    inlines = [CompositionInline]
    # αν έχεις slug στο μοντέλο:
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")

