from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Exhibit
from .serializers import UserSerializer, ExhibitSerializer
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth.hashers import check_password

class UserRegistration(APIView): #Rejestracja
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView): #logowanie
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Retrieve the user object from the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the provided password matches the hashed password
        if check_password(password, user.password):
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
class MakeAdminView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_admin = True
        user.save()
        return Response({'message': f'User {user.username} is now an admin'}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView): #wysiewtl wszstkich uzytkownikow 
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView): # wyswietl dane podanego uzytkownika 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_object(self):
        try:
            return self.get_queryset().get(username=self.kwargs.get('username'))
        except User.DoesNotExist:
            return Response({'error': f'User does not exist'}, status=404)

class CreateExhibitView(APIView): #swotrz eksponat
    def post(self, request):
        serializer = ExhibitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListExhibitsView(generics.ListAPIView): #lista wsztkich exponatow 
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer

class AddExhibitToUserView(APIView): #przypisanie eksponatu do uzytkoiwnika jako odwiedzony
    def post(self, request, username, exhibit_name):
        user = get_object_or_404(User, username=username)
        exhibit = get_object_or_404(Exhibit, name=exhibit_name)
        
        user.visited_exhibits.add(exhibit)
        user.calculate_points()
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VisitedExhibitsListView(generics.ListAPIView): #lista odwiedzonych eksponatow przez danego uzytkownika 
    serializer_class = ExhibitSerializer

    def get_queryset(self):
        try:
            username = self.kwargs['username']
            user = User.objects.get(username=username)
            return user.visited_exhibits.all()
        except User.DoesNotExist:
            return None
        
class TotalExhibitPointsView(APIView): #suma wsztkich punktow do zdobycia 
    def get(self, request):
        total_points = Exhibit.objects.aggregate(total_points=models.Sum('points'))['total_points']
        return Response({'total_points': total_points})

class ExhibitDeleteAPIView(APIView):
    def delete(request, pk):

        exhibit = Exhibit.objects.get(id=id)
        exhibit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

