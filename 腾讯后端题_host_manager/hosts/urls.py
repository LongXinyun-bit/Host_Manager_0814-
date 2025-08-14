from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet, IDCViewSet, HostViewSet, HostStatsViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'idcs', IDCViewSet)
router.register(r'hosts', HostViewSet)
router.register(r'stats', HostStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 