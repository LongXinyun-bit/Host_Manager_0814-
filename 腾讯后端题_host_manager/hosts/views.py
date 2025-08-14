from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from ping3 import ping

from .models import City, IDC, Host, HostStats
from .serializers import CitySerializer, IDCSerializer, HostSerializer, HostStatsSerializer
from .utils import decrypt_text


# Create your views here.


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer


class IDCViewSet(viewsets.ModelViewSet):
    queryset = IDC.objects.select_related('city').all().order_by('id')
    serializer_class = IDCSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.select_related('city', 'idc').all().order_by('id')
    serializer_class = HostSerializer

    @action(detail=True, methods=['post'])
    def ping(self, request, pk=None):
        host = self.get_object()
        try:
            rtt = ping(host.ip, unit='ms', timeout=1)
        except Exception:
            rtt = None
        host.ping_last_ok = bool(rtt)
        host.ping_last_rtt_ms = float(rtt) if rtt else None
        host.save(update_fields=['ping_last_ok', 'ping_last_rtt_ms', 'updated_at'])
        return Response({
            'ok': host.ping_last_ok,
            'rtt_ms': host.ping_last_rtt_ms,
            'timestamp': timezone.now(),
        })


class HostStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HostStats.objects.select_related('city', 'idc').all().order_by('-stat_date', 'city__name', 'idc__name')
    serializer_class = HostStatsSerializer
