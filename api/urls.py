from django.urls import path
from .views import UserRegistration, UserLogin, UserListView, UserDetailView, CreateExhibitView, ListExhibitsView, AddExhibitToUserView, VisitedExhibitsListView,TotalExhibitPointsView,ExhibitDeleteAPIView,MakeAdminView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_register'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('exhibits/', ListExhibitsView.as_view(), name='exhibit_list'),
    path('exhibits/total-points/', TotalExhibitPointsView.as_view(), name='total_exhibit_points'),
    path('exhibits/create/', CreateExhibitView.as_view(), name='exhibit_create'),
    path('users/<str:username>/exhibits/<str:exhibit_name>/', AddExhibitToUserView.as_view(), name='add_exhibit_to_user'),
    path('users/<str:username>/visited-exhibits/', VisitedExhibitsListView.as_view(), name='visited_exhibits_list'),
    path('exhibits-delete/<int:pk>/', ExhibitDeleteAPIView.as_view(), name='delete_exhibit'),
    path('users/<int:user_id>/make-admin/', MakeAdminView.as_view(), name='make_admin'),
]
