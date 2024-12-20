from rest_framework import serializers
from .models import Part
from .models import Team
from .models import Aircraft
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        part_name = data.get('name')
        team = data.get('team')
        aircraft = data.get('aircraft')

        if not user.teams.exists():
            raise serializers.ValidationError("You must belong to a team to create or edit a part.")

        if team not in user.teams.all():
            raise serializers.ValidationError("You can only create parts for your own team.")

        if part_name not in team.allowed_parts():
            raise serializers.ValidationError(f"The {team.name} cannot produce this part.")

        if part_name == 'wing' and aircraft not in ['tb2', 'tb3']:
            raise serializers.ValidationError("Wings can only be used for TB2 or TB3.")

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email'] 

class TeamSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True) 

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'users']

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

    def validate(self, data):
        aircraft_name = data['name']
        parts = data['parts']
        required_parts = ['wing', 'fuselage', 'tail', 'avionics']
        available_parts = [part.name for part in parts]

        for part in parts:
            if part.aircraft != aircraft_name:
                raise serializers.ValidationError(
                    f"{part.name} cannot be used for {aircraft_name}."
                )

        for required_part in required_parts:
            if required_part not in available_parts:
                raise serializers.ValidationError(f"Missing part: {required_part}")

        for part in parts:
            if part.team.name != 'assembly':
                raise serializers.ValidationError(f"{part.name} must be produced by the Assembly Team.")

        return data
    
class AircraftAssemblySerializer(serializers.Serializer):
    aircraft_name = serializers.ChoiceField(choices=[('tb2', 'TB2'), ('tb3', 'TB3'), ('akinci', 'AKINCI'), ('kizilelma', 'KIZILELMA')])

    def validate(self, data):
        user = self.context['request'].user
        assembly_team = user.teams.filter(name='assembly').first()
        if not assembly_team:
            raise serializers.ValidationError("You must be part of the Assembly Team to assemble an aircraft.")

        parts = data.get('parts', [])
        for part in parts:
            if part.team != assembly_team:
                raise serializers.ValidationError(f"Part {part.name} is not from the Assembly Team.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        assembly_team = user.teams.filter(name='assembly').first()

        try:
            return Aircraft.assemble_aircraft(validated_data['aircraft_name'], assembly_team)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user