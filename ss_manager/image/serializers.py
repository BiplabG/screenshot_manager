from wsgiref import validate
from rest_framework import serializers

from image.models import Image


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    height = serializers.IntegerField(read_only=True)
    width = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)

    image = serializers.ImageField(use_url=False, required=False)
    alt_text = serializers.CharField(
        allow_blank=True, max_length=120)

    def create(self, validatedData):
        return Image.objects.create(**validatedData)

    def update(self, instance, validatedData):
        instance.image = validatedData.get("image", instance.image)
        instance.alt_text = validatedData.get("alt_text", instance.alt_text)
        instance.save()
        return instance
