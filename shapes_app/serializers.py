from rest_framework import serializers
from .models import UserShape

class UserShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShape
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']