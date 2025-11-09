from django.contrib import admin
from .models import Venue, Concert, Composition


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "city")


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "venue", "is_public", "created_at")
    list_filter = ("is_public", "date", "venue")
    search_fields = ("title", "description")
    date_hierarchy = "date"


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("composer", "title", "order", "concert")
    list_filter = ("composer",)
    search_fields = ("composer", "title")


