from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Direction

User = get_user_model()

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    direction_ids = serializers.PrimaryKeyRelatedField(
        queryset=Direction.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    directions = DirectionSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "is_admin",
            "password",
            "direction_ids",   
            "directions",     
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        directions = validated_data.pop("direction_ids", [])
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if directions:
            user.directions.set(directions)
        return user

    def update(self, instance, validated_data):
        directions = validated_data.pop("direction_ids", None)
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if directions is not None:
            instance.directions.set(directions)
        return instance
