from django.db import models


class IdProvider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dh_legacy_id = models.CharField(blank=True, null=True, max_length=250)

    class Meta:
        abstract = True
