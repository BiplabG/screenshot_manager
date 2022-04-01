from rest_framework import serializers

from otp_auth.models import Otp


def validate_phone(value):
    splitted_data = value.split("-")
    if splitted_data[0] != "+977":
        raise serializers.ValidationError(
            "Currently, Nepal is the only country supported.")
    if len(splitted_data[1]) != 10:
        raise serializers.ValidationError(
            f"Invalid mobile number: {str(value)}"
        )


def validate_otp_value(value):
    if len(value) < 6:
        raise serializers.ValidationError(
            f"Invalid otp."
        )


class RequestOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32, validators=[validate_phone])


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32, validators=[validate_phone])
    otp_value = serializers.CharField(
        max_length=12, validators=[validate_otp_value])
