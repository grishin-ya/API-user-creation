from rest_framework import serializers
from .models import Trainee, Direction

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name']
        ref_name = 'DirectionSerializerTrainee'

class TraineeSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True, read_only=True)
    direction_ids = serializers.PrimaryKeyRelatedField(
        queryset=Direction.objects.all(),
        many=True,
        write_only=True,
        source='directions'
    )

    class Meta:
        model = Trainee
        fields = [
            'id', 'full_name', 'email', 'status', 'start_date', 'end_date',
            'rejection_reason', 'mentor', 'directions', 'direction_ids', 'created_at'
        ]

    def create(self, validated_data):
        directions = validated_data.pop('directions', [])
        trainee = Trainee.objects.create(**validated_data)
        trainee.directions.set(directions)
        return trainee

    def update(self, instance, validated_data):
        directions = validated_data.pop('directions', None)
        if directions is not None:
            instance.directions.set(directions)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
