from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Part, Team, User
from .models import Part, Team, User, Aircraft
from django.contrib.auth.models import User

class PartViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="password123")
        self.team = Team.objects.create(name="wing", description="Wing Team")
        self.team.users.add(self.user)
        
        self.other_team = Team.objects.create(name="fuselage", description="Fuselage Team")

        self.part_data = {
            "name": "wing",
            "quantity": 10,
            "team": self.team.id,
            "aircraft": "tb2",
        }

        self.client.force_authenticate(user=self.user)

    def test_create_part_valid(self):
        response = self.client.post("/api/parts/", self.part_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 1)
        self.assertEqual(Part.objects.first().name, "wing")

    def test_create_part_invalid_team(self):
        self.part_data["team"] = self.other_team.id
        response = self.client.post("/api/parts/", self.part_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You can only create parts for your own team.", str(response.data))

    def test_update_part_valid(self):
        part = Part.objects.create(
            name="wing", quantity=5, team=self.team, aircraft="tb2"
        )
        update_data = {
            "quantity": 15,
            "name": "wing",
            "team": self.team.id,
            "aircraft": "tb2"
        }        
        response = self.client.patch(f"/api/parts/{part.id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        part.refresh_from_db()
        self.assertEqual(part.quantity, 15)

    def test_delete_part_not_authenticated(self):
        self.client.logout()
        part = Part.objects.create(
            name="wing", quantity=5, team=self.team, aircraft="tb2"
        )
        response = self.client.delete(f"/api/parts/{part.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_part_valid(self):
        part = Part.objects.create(
            name="wing", quantity=5, team=self.team, aircraft="tb2"
        )
        response = self.client.delete(f"/api/parts/{part.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Part.objects.count(), 0)

class TeamViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Kullanıcı ve takım oluşturma
        self.user = User.objects.create_user(
            username="teamuser", email="teamuser@example.com", password="password123"
        )
        self.team = Team.objects.create(name="wing", description="Wing Team")
        self.team.users.add(self.user)

        self.other_user = User.objects.create_user(
            username="otheruser", email="otheruser@example.com", password="password123"
        )

        self.client.force_authenticate(user=self.user)

    def test_add_user_to_team(self):
        """Takıma yeni bir kullanıcı ekleme testi."""
        response = self.client.post(
            f"/api/teams/{self.team.id}/add_user/",
            {"email": self.other_user.email},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.other_user, self.team.users.all())

    def test_add_existing_user_to_team(self):
        """Takıma zaten eklenmiş bir kullanıcıyı tekrar ekleme testi."""
        self.team.users.add(self.other_user) 
        response = self.client.post(
            f"/api/teams/{self.team.id}/add_user/",
            {"email": self.other_user.email},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User is already in this team.", str(response.data))

    def test_remove_user_from_team(self):
        """Takımdan bir kullanıcıyı çıkarma testi."""
        self.team.users.add(self.other_user) 
        response = self.client.delete(
            f"/api/teams/{self.team.id}/remove_user/",
            {"user_id": self.other_user.id},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.other_user, self.team.users.all())

class AircraftViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="aircraftuser", password="password123")
        self.client.force_authenticate(user=self.user)

        self.team = Team.objects.create(name="assembly", description="Assembly Team")
        self.team.users.add(self.user)

        self.part1 = Part.objects.create(name="wing", quantity=1, team=self.team, aircraft="tb2", is_used=False)
        self.part2 = Part.objects.create(name="fuselage", quantity=1, team=self.team, aircraft="tb2", is_used=False)
        self.part3 = Part.objects.create(name="tail", quantity=1, team=self.team, aircraft="tb2", is_used=False)
        self.part4 = Part.objects.create(name="avionics", quantity=1, team=self.team, aircraft="tb2", is_used=False)

        self.aircraft_data = {
            "name": "tb2",
            "parts": [self.part1.id, self.part2.id, self.part3.id, self.part4.id],
        }

    def test_create_aircraft_valid(self):
        response = self.client.post("/api/aircrafts/", self.aircraft_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Aircraft.objects.count(), 1)
        self.assertEqual(Aircraft.objects.first().name, "tb2")

    def test_create_aircraft_missing_parts(self):
        self.aircraft_data["parts"] = [self.part1.id, self.part2.id]
        response = self.client.post("/api/aircrafts/", self.aircraft_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing part", str(response.data))

    def test_create_aircraft_invalid_team(self):
        other_team = Team.objects.create(name="fuselage", description="Fuselage Team")
        self.part1.team = other_team
        self.part1.save()

        response = self.client.post("/api/aircrafts/", self.aircraft_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("wing must be produced by the Assembly Team.", str(response.data))
