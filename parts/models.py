from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Team(models.Model):
    TEAM_CHOICES = [
        ('wing', 'Wing Team'),
        ('fuselage', 'Fuselage Team'),
        ('tail', 'Tail Team'),
        ('avionics', 'Avionics Team'),
        ('assembly', 'Assembly Team'),
    ]

    name = models.CharField(max_length=50, choices=TEAM_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return self.get_name_display()

    def allowed_parts(self):
        """
        Takımın üretebileceği parça türlerini döner.
        """
        allowed_parts_map = {
            'wing': ['wing'],
            'fuselage': ['fuselage'],
            'tail': ['tail'],
            'avionics': ['avionics'],
            'assembly': [],
        }
        return allowed_parts_map.get(self.name, [])

class Part(models.Model):
    PART_CHOICES = [
        ('wing', 'Wing'),
        ('fuselage', 'Fuselage'),
        ('tail', 'Tail'),
        ('avionics', 'Avionics'),
    ]

    name = models.CharField(max_length=50, choices=PART_CHOICES)
    quantity = models.PositiveIntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='parts')
    is_used = models.BooleanField(default=False) 

    aircraft = models.CharField(
        max_length=50,
        choices=[
            ('tb2', 'TB2'),
            ('tb3', 'TB3'),
            ('akinci', 'AKINCI'),
            ('kizilelma', 'KIZILELMA'),
        ],
    )

    def __str__(self):
        return f"{self.get_name_display()} for {self.get_aircraft_display()}"
    
    def mark_as_used(self):
        if self.is_used:
            raise ValidationError(f"{self.get_name_display()} has already been used.")
        self.is_used = True
        self.save()

    def clean(self):
        """
        Parçanın belirlenen uçak modeline uygun olup olmadığını doğrular.
        """
        valid_parts_map = {
            'wing': ['tb2', 'tb3'],
            'fuselage': ['tb2', 'tb3', 'akinci'],
            'tail': ['tb2', 'tb3', 'akinci'],
            'avionics': ['tb2', 'tb3', 'akinci', 'kizilelma']
        }
        
        if self.aircraft not in valid_parts_map.get(self.name, []):
            raise ValidationError(f"{self.get_name_display()} can only be used for {', '.join(valid_parts_map.get(self.name, []))}.")
        
class Aircraft(models.Model):
    AIRCRAFT_CHOICES = [
        ('tb2', 'TB2'),
        ('tb3', 'TB3'),
        ('akinci', 'AKINCI'),
        ('kizilelma', 'KIZILELMA'),
    ]

    name = models.CharField(max_length=50, choices=AIRCRAFT_CHOICES, unique=True)
    parts = models.ManyToManyField(Part, related_name='aircrafts')
    produced_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_name_display()
    
    def __str__(self):
        return self.get_name_display()
    
    @classmethod
    def assemble_aircraft(cls, aircraft_name, assembly_team):
        """
        Tüm gerekli parçaları kontrol ederek bir uçak montajı gerçekleştirir.
        """
        required_parts = ['wing', 'fuselage', 'tail', 'avionics']
        available_parts = Part.objects.filter(
            team=assembly_team, 
            is_used=False,
            name__in=required_parts
        )

        missing_parts = [part for part in required_parts if part not in available_parts.values_list('name', flat=True)]
        if missing_parts:
            raise ValueError(f"Missing parts: {', '.join(missing_parts)}")

        aircraft = cls.objects.create(name=aircraft_name)
        for part in available_parts:
            part.mark_as_used()
            aircraft.parts.add(part)

        return aircraft
