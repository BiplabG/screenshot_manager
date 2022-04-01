from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from otp_auth.serializers import RequestOtpSerializer, VerifyOtpSerializer
from otp_auth.models import Otp, PhoneUser, User

# Create your views here.


class RequestOtp(APIView):
    def get_object(self, phone):
        try:
            otp = Otp.objects.get(phone=phone)
            return otp
        except Otp.DoesNotExist:
            return None

    def post(self, request, format=None):
        serializer = RequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            previous_otp_instance = self.get_object(
                phone=serializer.data["phone"])
            if previous_otp_instance:
                previous_otp_instance.delete()

            # TODO: Generate random otp_value
            otp_instance = Otp(otp_value="123456",
                               phone=serializer.data["phone"])
            # TODO: Send OTP via appropriate SMS provider
            otp_instance.save()
            return Response({"message": "OTP sent to your mobile successfully."})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    def get_object(self, phone):
        otp = Otp.objects.get(phone=phone)
        return otp

    def get_user_object(self, phone):
        try:
            phone_user = PhoneUser.objects.get(phone=phone)
            return phone_user
        except PhoneUser.DoesNotExist:
            return None

    def get_token_object(self, user):
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except PhoneUser.DoesNotExist:
            return None
        token = Token.objects.create(user=user)
        return token

    def post(self, request, format=None):
        try:
            serializer = VerifyOtpSerializer(data=request.data)
            if serializer.is_valid():
                otp_instance = self.get_object(phone=serializer.data["phone"])
                # TODO: Also check if otp is expired or not
                if otp_instance.otp_value == serializer.data["otp_value"]:
                    otp_instance.delete()
                    phone_user = self.get_user_object(
                        phone=serializer.data["phone"])
                    if not phone_user:
                        user = User.objects.create_user(
                            username=serializer.data["phone"])
                        user.set_unusable_password()
                        phone_user = PhoneUser(
                            user=user, phone=serializer.data["phone"])
                        phone_user.save()

                    token = self.get_token_object(user=phone_user.user)
                    return Response({"message": "OTP verified successfully.", "token": str(token.key)})
                else:
                    return Response({"message": "Incorrect OTP. Could not verify the account."})

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Otp.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogOut(APIView):
    def post(self, request, format=None):
        pass
