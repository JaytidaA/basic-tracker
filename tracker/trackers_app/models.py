from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Create your models here.

class Tracking(models.Model):
    class Kind(models.TextChoices):
        ELIMINATION = "elim", "Elimination (out on first entry)"
        SUM = "sum", "Running Total"

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=10, choices=Kind.choices)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="trackings")
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null = True, blank = True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.name}"

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries")
    tracking = models.ForeignKey(Tracking, on_delete=models.CASCADE, related_name="entries")
    occurred_at = models.DateTimeField(default=timezone.now)
    value = models.PositiveIntegerField(default=1) # 1 for elimination type contests
    details = models.TextField(blank=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [models.Index(fields=["tracking", "user"])]
        verbose_name_plural = "entries"

    def clean(self):
        if not self.tracking.members.filter(pk=self.user_id).exists():
            raise ValidationError("User is not a member of this tracking.")
        if self.tracking.kind == Tracking.Kind.ELIMINATION:
            already_out = (Entry.objects
                           .filter(tracking=self.tracking, user=self.user)
                           .exclude(pk=self.pk).exists())
            if already_out:
                raise ValidationError("Already eliminated")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} @ {self.tracking} ({self.occurred_at:%Y-%m-%d})"
