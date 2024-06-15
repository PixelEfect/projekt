from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import User, Exhibit, Room, Comment
from .serializers import UserSerializer, ExhibitSerializer, RoomSerializer, CommentSerializer
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Sum
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

class ExhibitUpdateView(generics.UpdateAPIView):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer
    lookup_field = 'id'

# Widok błędów przy rejestracji
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Logowanie błędów
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(APIView): # Rejestracja
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView): # Logowanie
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

class UserListView(generics.ListAPIView): # Wyświetl wszystkich użytkowników 
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView): # Wyświetl dane podanego użytkownika 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_object(self):
        try:
            return self.get_queryset().get(username=self.kwargs.get('username'))
        except User.DoesNotExist:
            return Response({'error': f'User does not exist'}, status=404)

class CreateExhibitView(APIView): # Stwórz eksponat
    def post(self, request):
        serializer = ExhibitSerializer(data=request.data)
        if serializer.is_valid():
            room_number = request.data.get('room')
            if not Room.objects.filter(room_number=room_number).exists():
                return Response({'error': f'Room with number {room_number} does not exist.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListExhibitsView(generics.ListAPIView): # Lista wszystkich eksponatów 
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer

class AddExhibitToUserView(APIView): # Przypisanie eksponatu do użytkownika jako odwiedzony
    def post(self, request, username, exhibit_name):
        user = get_object_or_404(User, username=username)
        exhibit = get_object_or_404(Exhibit, name=exhibit_name)
        
        user.visited_exhibits.add(exhibit)
        # user.calculate_points()
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VisitedExhibitsListView(generics.ListAPIView): # Lista odwiedzonych eksponatów przez danego użytkownika 
    serializer_class = ExhibitSerializer

    def get_queryset(self):
        try:
            username = self.kwargs['username']
            user = User.objects.get(username=username)
            return user.visited_exhibits.all()
        except User.DoesNotExist:
            return None

class TotalExhibitPointsView(APIView): # Suma wszystkich punktów do zdobycia 
    def get(self, request):
        total_points = Exhibit.objects.aggregate(total_points=models.Sum('points'))['total_points']
        return Response({'total_points': total_points})

class ExhibitDeleteAPIView(APIView):
    def delete(request, pk):
        exhibit = Exhibit.objects.get(id=id)
        exhibit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateRoomView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

def update_exhibit(request, pk):
    try:
        exhibit = Exhibit.objects.get(pk=pk)
    except Exhibit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ExhibitSerializer(exhibit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_comment(request):
    user_id = request.data.get('user_id')
    exhibit_id = request.data.get('exhibit_id')
    comment_text = request.data.get('comment')

    if not user_id or not exhibit_id or not comment_text:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
        exhibit = Exhibit.objects.get(id=exhibit_id)
    except (User.DoesNotExist, Exhibit.DoesNotExist):
        return Response({'error': 'User or Exhibit not found'}, status=status.HTTP_404_NOT_FOUND)

    comment, created = Comment.objects.update_or_create(
        user=user,
        exhibit=exhibit,
        defaults={'comment': comment_text}
    )

    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK if created else status.HTTP_201_CREATED)

def get_user_id(request, username):
    try:
        user = User.objects.get(username=username)
        return JsonResponse({'id': user.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def user_details(request, username):
    user = get_object_or_404(User, username=username)
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'total_museum_points': user.total_museum_points,
        # Add other necessary fields
    }
    return JsonResponse(data)

def get_user_points(request, username):
    user = User.objects.get(username=username)
    user.calculate_total_museum_points()  # Obliczanie punktów użytkownika
    return JsonResponse({'username': user.username, 'total_museum_points': user.total_museum_points})

def total_available_points(request):
    total_points = Exhibit.objects.aggregate(total_points=Sum('points'))['total_points']
    data = {
        'total_points': total_points
    }
    return JsonResponse(data)

@api_view(['GET'])
def get_comments(request, exhibit_id):
    comments = Comment.objects.filter(exhibit_id=exhibit_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

