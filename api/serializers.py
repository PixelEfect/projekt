from rest_framework import serializers
from .models import User, Exhibit, Room, Comment
from django.contrib.auth.hashers import make_password # sluzy do hashowania hasla 

class ExhibitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibit
        fields = ['id', 'name', 'description', 'points', 'room']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'exhibit', 'comment']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    visited_exhibits = ExhibitSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'visited_exhibits', 'total_museum_points', 'room_points', 'is_admin']
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        instance = super().create(validated_data)
        instance.calculate_total_museum_points()
        return instance
