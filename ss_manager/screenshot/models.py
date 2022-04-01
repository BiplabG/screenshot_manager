from django.db import models

# Create your models here.


class Screenshot(models.Model):
    title = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        'image.Image', on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    is_edited = models.BooleanField(default=False, editable=False)
    is_archived = models.BooleanField(default=False, editable=False)

    user = models.ForeignKey(
        "otp_auth.User", related_name="screenshots", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
