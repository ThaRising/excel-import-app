from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class EmailTokenObtainSerializer(  # noqa must implement abstract
    TokenObtainSerializer
):
    username_field = get_user_model().EMAIL_FIELD


class TokenObtainQuerySerializer(  # noqa must implement abstract
    serializers.Serializer
):
    only = serializers.ChoiceField(
        choices=[
            ("access", "Access-Token"),
            ("both", "Access-Token & Refresh-Token")
        ],
        default="both"
    )


class CustomTokenObtainPairSerializer(  # noqa must implement abstract
    EmailTokenObtainSerializer
):
    query_serializer = TokenObtainQuerySerializer
    args_for_query = ("only",)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    @classmethod
    def get_access_token(cls, user):
        return AccessToken.for_user(user)

    def validate(self, attrs: dict):
        query = {
            k: v for k in self.args_for_query if (
                v := self.initial_data.pop(k, None)
            )
        }
        data = super().validate(attrs)
        query_serializer = self.query_serializer(data=query)
        query_serializer.is_valid(raise_exception=True)
        query = query_serializer.validated_data.get("only")

        if query == "access":
            token = self.get_access_token(self.user)
            data["access"] = str(token)
        elif query == "both":
            refresh = self.get_token(self.user)
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

        return data


class ObtainSchema(serializers.Serializer):  # noqa must implement abstract
    access = serializers.CharField(required=True)
    refresh = serializers.CharField(required=False)


class RefreshSchema(serializers.Serializer):  # noqa must implement abstract
    access = serializers.CharField(required=True)


class TokenDestroySchema(serializers.Serializer):  # noqa must implement abstract
    refresh = serializers.CharField(required=True)
