from rest_framework.routers import DefaultRouter
from .views import PartViewSet
from .views import TeamViewSet
from .views import AircraftViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='part')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'aircrafts', AircraftViewSet, basename='aircraft')

urlpatterns = [
    path('', include(router.urls)),
]