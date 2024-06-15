from django.urls import path
from .views import (
    RegisterView, CreateRoomView, RoomListView, ExhibitUpdateView, get_user_id,
    add_comment, get_comments, UserRegistration, UserLogin, UserListView, UserDetailView,
    CreateExhibitView, ListExhibitsView, AddExhibitToUserView, VisitedExhibitsListView,
    TotalExhibitPointsView, ExhibitDeleteAPIView, MakeAdminView
)
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Sprawdzanie błędów przy rejestracji
    path('register/', UserRegistration.as_view(), name='user_register'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('api/add_comment/', add_comment, name='add_comment'),
        path('add_comment/', add_comment, name='add_comment'),
    path('users/<str:username>/id/', get_user_id, name='get_user_id'),
    path('api/users/<str:username>/id/', get_user_id, name='get_user_id'),
    path('api/comments/<int:exhibit_id>/', get_comments, name='get_comments'),
    path('comments/<int:exhibit_id>/', get_comments, name='get_comments'),
    path('api/users/<str:username>/', views.user_details, name='user_details'),
    path('api/exhibits/total-points/', views.total_available_points, name='total_available_points'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('exhibits/<int:id>/', ExhibitUpdateView.as_view(), name='exhibit_update'),
    path('api/exhibits/<int:id>/', ExhibitUpdateView.as_view(), name='exhibit_update'),
    path('exhibits/<int:pk>/update/', views.update_exhibit, name='update_exhibit'),
    path('rooms/create/', CreateRoomView.as_view(), name='create_room'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('api/rooms/', RoomListView.as_view(), name='room_list'),
    path('api/exhibits/create/', CreateExhibitView.as_view(), name='create_exhibit'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('exhibits/', ListExhibitsView.as_view(), name='exhibit_list'),
    path('exhibits/total-points/', TotalExhibitPointsView.as_view(), name='total_exhibit_points'),
    path('exhibits/create/', CreateExhibitView.as_view(), name='exhibit_create'),
    path('users/<str:username>/exhibits/<str:exhibit_name>/', AddExhibitToUserView.as_view(), name='add_exhibit_to_user'),
    path('users/<str:username>/visited-exhibits/', VisitedExhibitsListView.as_view(), name='visited_exhibits_list'),
    path('exhibits-delete/<int:pk>/', ExhibitDeleteAPIView.as_view(), name='delete_exhibit'),
    path('users/<int:user_id>/make-admin/', MakeAdminView.as_view(), name='make_admin'),
]

