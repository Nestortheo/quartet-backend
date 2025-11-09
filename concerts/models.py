from django.db import models

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
    date = models.DateTimeField()
    venue = models.ForeignKey(Venue, related_name='concerts', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    ticket_link = models.URLField(blank=True, null=True)
    event_link = models.URLField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.venue.name} - {self.date.strftime('%Y-%m-%d')}"

#For Compositions↔Concert: many compositions belong to one concert → FK on Composition.
class Composition(models.Model):
    concert = models.ForeignKey(Concert, related_name='program', on_delete=models.CASCADE)
    composer = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.composer}: {self.title}"
