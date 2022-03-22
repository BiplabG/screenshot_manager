from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from image.models import Image
from image.serializers import ImageSerializer


class ImageList(APIView):
    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            image = request.data["image"]
        except KeyError:
            raise Exception("Request has no image attached.")

        data = {
            "alt_text": request.data.get("alt_text"),
            "image": image,
        }
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    def get_object(self, pk):
        try:
            image = Image.objects.get(pk=pk)
            return image
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            if request.data.get("image"):
                image.image.delete(save=False)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        image.image.delete(save=False)
        return Response(status=status.HTTP_204_NO_CONTENT)
