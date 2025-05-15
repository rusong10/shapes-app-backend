from rest_framework import serializers
from .models import Shape

class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shape
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']