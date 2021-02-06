from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        required=True, validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all()
            )
        ]
    )
    password = serializers.CharField(
        min_length=8,
        max_length=50,
        write_only=True,
        required=True
    )
    first_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=False,
        allow_null=True
    )
    last_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=False,
        allow_null=True
    )

    def create(self, validated_data):
        model = get_user_model()
        return model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            new_password = validated_data.pop("password")
            instance.set_password(new_password)

        for field_name, value in validated_data.items():
            setattr(
                instance,
                field_name,
                value
            )

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get("first_name"):
            data["first_name"] = None
        if not data.get("last_name"):
            data["last_name"] = None
        return data
