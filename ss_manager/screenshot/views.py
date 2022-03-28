from copy import deepcopy
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from screenshot.models import Screenshot
from screenshot.serializers import ScreenshotSerializer
from image.helpers import get_image_detail
from screenshot.permissions import IsOwnerOrReadOnly


class ScreenshotList(APIView):
    permission_classes = [
        permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Screenshot.objects.filter(user=user)

    def get(self, request, format=None):
        screenshots = self.get_queryset()
        serializer = ScreenshotSerializer(screenshots, many=True)
        screenshot_list = serializer.data
        for i, _ in enumerate(serializer.data):
            screenshot_list[i]['image'] = get_image_detail(
                serializer.data[i]['image'])
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScreenshotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreenshotDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            screenshot = Screenshot.objects.get(pk=pk)
            self.check_object_permissions(self.request, screenshot)
            return screenshot
        except Screenshot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        screenshot = self.get_object(pk)
        serializer = ScreenshotSerializer(screenshot)
        screenshot_data = deepcopy(serializer.data)

        screenshot_data["image"] = get_image_detail(
            slug=screenshot_data.pop("image"))
        return Response(screenshot_data)

    def put(self, request, pk, format=None):
        screenshot = self.get_object(pk)
        serializer = ScreenshotSerializer(screenshot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        screenshot = self.get_object(request, pk)
        screenshot.delete()
        # TODO: Also delete the associated image
        return Response(status=status.HTTP_204_NO_CONTENT)
