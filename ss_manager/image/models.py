from django.db import models

# Create your models here.


class Image(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to="uploads/images/", height_field="height", width_field="width"
    )
    # image_thumbnail = models.ImageField(upload_to="images/")
    height = models.PositiveIntegerField(editable=False)
    width = models.PositiveIntegerField(editable=False)
    alt_text = models.CharField(blank=True, max_length=120)

    # TODO: Authenticate and authorize image access.
