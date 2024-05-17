from rest_framework import serializers
from .models import User, Exhibit
from django.contrib.auth.hashers import make_password # sluzy do hashowania hasla 

class ExhibitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibit
        fields = ['id', 'name', 'description','points']


class UserSerializer(serializers.ModelSerializer):
    visited_exhibits = ExhibitSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'visited_exhibits','points','is_admin']
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        instance = super().create(validated_data)
        instance.calculate_points()
        return instance
