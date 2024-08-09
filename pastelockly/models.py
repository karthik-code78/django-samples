from django.db import models

# Create your models here.
class PasteLock(models.Model):
    id = models.AutoField(primary_key=True)
    text_field = models.TextField(null=False, blank=False)
    password_field = models.CharField(max_length=16, null=True, blank=True)
    is_locked = models.BooleanField(default=False)