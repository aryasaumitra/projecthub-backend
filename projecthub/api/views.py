from django.http import JsonResponse
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(APIView):
    """
    Register the user by sending the following format in body:
    {
        "username":"",
        "password":"",
        "is_staff":True/False
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                username=data['username'],
                password=make_password(data['password']),
                is_staff=data.get('is_staff', False),  # For role-based access
            )
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (request.user.is_staff or request.method in ['GET'])
    
class IsUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.method in ['GET']
    


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = PageNumberPagination

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUser]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'status']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Task.objects.filter(assigned_to=self.request.user)
        return Task.objects.all()
    
class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


def root_view(request):
    return JsonResponse({
        "message": "Welcome to the Project Hub API",
        "status": "Server is running",
        "documentation": "http://127.0.0.1:8000/swagger/"
    })



