from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField(blank=True)        # optional, if you want full address
    map_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.city}"

#For Concerts↔Venue: many concerts belong to one venue → FK on Concert.
class Concert(models.Model):
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    date_start = models.DateTimeField(db_index=True)
    date_end = models.DateTimeField(null=True, blank=True)
    venue = models.ForeignKey("Venue", related_name="concerts", on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    ticket_link = models.URLField(blank=True, null=True)
    event_link = models.URLField(blank=True, null=True)
    is_public = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_start", "-id"]

    def __str__(self):
        return f"{self.title or 'Concert'} — {self.venue.name} — {self.date_start:%Y-%m-%d}"

    # ✅ Validation: ensure date_end is after date_start
    def clean(self):
        if self.date_end and self.date_end < self.date_start:
            raise ValidationError("date_end must be after date_start")

    # ✅ Auto-generate slug & avoid duplicates
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title or f"{self.venue.name}-{self.date_start:%Y-%m-%d}")
            s = base
            n = 1
            while Concert.objects.filter(slug=s).exclude(pk=self.pk).exists():
                n += 1
                s = f"{base}-{n}"
            self.slug = s
        super().save(*args, **kwargs)



#For Compositions↔Concert: many compositions belong to one concert → FK on Composition.
class Composition(models.Model):
    concert = models.ForeignKey(Concert, related_name='program', on_delete=models.CASCADE)
    composer = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=["concert", "order"], name="uniq_program_order_per_concert"),
        ]

    def __str__(self):
        return f"{self.composer}: {self.title}"
