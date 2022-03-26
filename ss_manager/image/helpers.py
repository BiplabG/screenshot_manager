from image.models import Image
from image.serializers import ImageSerializer

def get_image_detail(slug):
    image = Image.objects.get(slug=slug)
    image_serializer = ImageSerializer(image)
    return image_serializer.data
