from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from screenshot.models import Screenshot
from screenshot.serializers import ScreenshotSerializer


class ScreenshotList(APIView):
    def get(self, request, format=None):
        screenshots = Screenshot.objects.all()
        serializer = ScreenshotSerializer(screenshots, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScreenshotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreenshotDetail(APIView):
    def get_object(self, pk):
        try:
            screenshot = Screenshot.objects.get(pk=pk)
            return screenshot
        except Screenshot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        screenshot = self.get_object(pk)
        serializer = ScreenshotSerializer(screenshot)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        screenshot = self.get_object(pk)
        serializer = ScreenshotSerializer(screenshot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        screenshot = self.get_object(pk)
        screenshot.delete()
        # TODO: Also delete the associated image
        return Response(status=status.HTTP_204_NO_CONTENT)
