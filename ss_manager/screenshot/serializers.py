from rest_framework import serializers
from screenshot.models import Screenshot
from image.models import Image


class ScreenshotSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    is_edited = serializers.BooleanField(read_only=True)
    is_archived = serializers.BooleanField(read_only=True)

    title = serializers.CharField(allow_blank=True, max_length=120)
    description = serializers.CharField(allow_blank=True)
    image = serializers.SlugRelatedField(
        slug_field="slug", queryset=Image.objects.all())
    user = serializers.ReadOnlyField(source='user.username')

    def create(self, validatedData):
        print(validatedData)
        return Screenshot.objects.create(**validatedData)

    def update(self, instance, validatedData):
        instance.title = validatedData.get("title", instance.title)
        instance.description = validatedData.get(
            "description", instance.description)
        instance.is_edited = True
        instance.save()
        return instance
