from rest_framework.viewsets import ModelViewSet
from .models import Part
from .serializers import PartSerializer
from .models import Team
from .serializers import TeamSerializer
from .models import Aircraft
from .serializers import AircraftSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .serializers import AircraftAssemblySerializer
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny 
from .models import User

class PartViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        return Part.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        team = serializer.validated_data.get('team')
        part_name = serializer.validated_data.get('name')

        if team not in user.teams.all():
            raise PermissionDenied("You can only create parts for your own team.")

        if part_name not in team.allowed_parts():
            raise PermissionDenied(f"The {team.name} cannot produce this part.")
        
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        team = serializer.validated_data.get('team')

        if team not in user.teams.all():
            raise PermissionDenied("You can only update parts for your own team.")
        
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be authenticated to delete a part.")
        if instance.team not in user.teams.all():
            raise PermissionDenied("You can only delete parts from your own team.")
        instance.delete()

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        part = self.get_object()
        return Response({
            "name": part.name,
            "quantity": part.quantity,
            "is_used": part.is_used,
            "aircraft": part.aircraft,
            "team": part.team.name if part.team else None,
        })


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'])
    def add_user(self, request, *args, **kwargs):
        team = self.get_object() 
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if team.users.filter(id=user.id).exists():
            return Response({"error": "User is already in this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        team.users.add(user)
        return Response({"message": "User added to team successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def remove_user(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if not team.users.filter(id=user.id).exists():
            return Response({"error": "User is not in this team."}, status=status.HTTP_400_BAD_REQUEST)
        team.users.remove(user)
        return Response({"message": "User removed from team successfully."}, status=status.HTTP_200_OK)

class AircraftViewSet(ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = [] 

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AircraftAssemblyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AircraftAssemblySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            aircraft = serializer.save()
            return Response(
                {"message": f"{aircraft.name} has been successfully assembled."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    